#include <stdbool.h>
#include <stdint.h>
#include "nordic_common.h"
#include "bsp.h"
#include "nrf_soc.h"
#include "nrf_sdh.h"
#include "nrf_sdh_ble.h"
#include "ble_advdata.h"
#include "app_timer.h"
#include "nrf_pwr_mgmt.h"
#include "nrf_delay.h"

#define ARRAY_LENGTH(array) (uint8_t)sizeof(array)

#define APP_BLE_CONN_CFG_TAG            1  /**< A tag identifying the SoftDevice BLE configuration. */

#define NON_CONNECTABLE_ADV_INTERVAL    MSEC_TO_UNITS(100, UNIT_0_625_MS)   // The advertising interval in multiples of 0.625 ms. This value can vary between 100ms to 10.24s
#define NON_CONNECTABLE_ADV_TIMEOUT     MSEC_TO_UNITS(4000, UNIT_10_MS)     // The advertising timeout in multiples of 10 ms. 0 means no timeout. 
#define NON_CONNECTABLE_ADV_LIMIT       100   // Maximum number of advertising atempts. After this limit is reached, a timeout event is triggered. 

/* Definition of the Advertising packet. 
  It is formed of N sub-packets, each conformed by 1 byte of size (type+data) + 1 byte of type + n bytes of data. 
  The total payload must not exced 31 bytes. 
*/
#define APP_AD_LEN_FLAG     ARRAY_LENGTH(((uint8_t[]){APP_AD_TYPE_FLAG,APP_AD_DATA_FLAG})) 
#define APP_AD_TYPE_FLAG    0X01
#define APP_AD_DATA_FLAG    0X06    // Nonconnectable, undirected 
#define APP_AD_LEN_MSD      ARRAY_LENGTH(((uint8_t[]){APP_AD_TYPE_MSD,APP_AD_DATA_MSD})) 
#define APP_AD_TYPE_MSD     0XFF
#define APP_AD_DATA_MSD     0X59,0x00  // Nordic Semiconductors
#define APP_AD_LEN_SHLN     ARRAY_LENGTH(((uint8_t[]){APP_AD_TYPE_SHLN,APP_AD_DATA_SHLN})) 
#define APP_AD_TYPE_SHLN    0x08    // Shortened Local Name   
#define APP_AD_DATA_SHLN    0x31,0x32,0x33,0x34,0x35,0x36,0x37,0x38,0x39,0x41,0x42,0X43,0X44,0x45  // ID on the Tag

// The advertising data is concatenated into one single array. 
static uint8_t advData[BLE_GAP_ADV_SET_DATA_SIZE_MAX] = {
   APP_AD_LEN_FLAG,     
   APP_AD_TYPE_FLAG,    
   APP_AD_DATA_FLAG, 
   APP_AD_LEN_MSD,      
   APP_AD_TYPE_MSD,     
   APP_AD_DATA_MSD,     
   APP_AD_LEN_SHLN,      
   APP_AD_TYPE_SHLN,    
   APP_AD_DATA_SHLN 
};

static ble_gap_adv_params_t m_adv_params;                                  /**< Parameters to be passed to the stack when starting advertising. */
static uint8_t              m_adv_handle = BLE_GAP_ADV_SET_HANDLE_NOT_SET; /**< Advertising handle used to identify an advertising set. */

// The advertising data structure to be used to initialize the the advertising set
static ble_gap_adv_data_t m_adv_data ={
    .adv_data =
    {
        .p_data = advData, //The data to be used in the advertising packet must be already encoded (all sub-packets in the length+type+data form)
        .len    = BLE_GAP_ADV_SET_DATA_SIZE_MAX
    },
};

/*
  This function lowers all pins and puts the module to deep sleep mode:
  leaves one pin to be used as wake-up source and then turns the device off. 
  Once the device is on, it shall restart itself. Nothing is excecuted after 
  sd_power_system_off() unless it fails. 
*/
static void goto_sleep(void){
    uint32_t err_code;

    // Set all pins to GND
    bsp_board_led_off(2);
    bsp_board_led_on(1);

    //configure button 0 for wakeup
    nrf_gpio_cfg_sense_input(BSP_BUTTON_0, GPIO_PIN_CNF_PULL_Pullup, GPIO_PIN_CNF_SENSE_Low);
    
    // Go to system-off mode (this function will not return; wakeup will cause a reset).
    err_code = sd_power_system_off();
    APP_ERROR_CHECK(err_code);
}


/*
  This function is the oberver for all BLE events. Each event has an unique identifier. 
  The BLE_GAP_EVT_ADV_SET_TERMINATED ID means the advertising set has finished, either by 
  timeout or because the maximum number of advertising iterations has been reached.
*/
static void ble_evt_handler(ble_evt_t const * p_ble_evt, void * p_context){
  if ( p_ble_evt->header.evt_id == BLE_GAP_EVT_ADV_SET_TERMINATED) {
    goto_sleep(); // Once the advertising set is terminated, the device should go to sleep.
  }
}

/*
  During the initialization of the advertising set, configuration parameters are set and passed
  to the adv_set_configure function. The advertising data to be contained in the packet should also
  be passed (already encoded).
*/
static void advertising_init(void){
    uint32_t      err_code;

    memset(&m_adv_params, 0, sizeof(m_adv_params));
    m_adv_params.properties.type = BLE_GAP_ADV_TYPE_NONCONNECTABLE_NONSCANNABLE_UNDIRECTED; // The type of operation the node will have. Non-non-un consumed the least energy.
    m_adv_params.p_peer_addr     = NULL;    // Undirected advertisement.
    m_adv_params.filter_policy   = BLE_GAP_ADV_FP_ANY; // No filter
    m_adv_params.interval        = NON_CONNECTABLE_ADV_INTERVAL;  // Interval between advertising iterations
    m_adv_params.duration        = NON_CONNECTABLE_ADV_TIMEOUT;   // Max time between advertising start and termination of set.
    m_adv_params.max_adv_evts    = NON_CONNECTABLE_ADV_LIMIT;     // Max advertising iterations between start and termination of set
    
    err_code = sd_ble_gap_adv_set_configure(&m_adv_handle, &m_adv_data, &m_adv_params);
    APP_ERROR_CHECK(err_code);

    // An observer is declared, under the name of m_ble_observer, with prioriry 3, and that shall be attended by ble_evt_handler.
    // At each BLE event, the handler function will be called. 
    NRF_SDH_BLE_OBSERVER(m_ble_observer, 3, ble_evt_handler, NULL);
}

// Effectively start transmitting advertising packets
static void advertising_start(void){
    ret_code_t err_code;

    err_code = sd_ble_gap_adv_start(m_adv_handle, APP_BLE_CONN_CFG_TAG);
    APP_ERROR_CHECK(err_code);

    err_code = bsp_indication_set(BSP_INDICATE_ADVERTISING);
    APP_ERROR_CHECK(err_code);

}


static void ble_stack_init(void){
    ret_code_t err_code;

    err_code = nrf_sdh_enable_request();
    APP_ERROR_CHECK(err_code);

    // Configure the BLE stack using the default settings.
    // Fetch the start address of the application RAM.
    uint32_t ram_start = 0;
    err_code = nrf_sdh_ble_default_cfg_set(APP_BLE_CONN_CFG_TAG, &ram_start);
    APP_ERROR_CHECK(err_code);

    // Enable BLE stack.
    err_code = nrf_sdh_ble_enable(&ram_start);
    APP_ERROR_CHECK(err_code);

    
}

static void leds_init(void){
    ret_code_t err_code = bsp_init(BSP_INIT_LEDS, NULL);
    APP_ERROR_CHECK(err_code);
}

static void timers_init(void){
    ret_code_t err_code = app_timer_init();
    APP_ERROR_CHECK(err_code);
}

static void power_management_init(void){
    ret_code_t err_code;
    err_code = nrf_pwr_mgmt_init();
    APP_ERROR_CHECK(err_code);
}

static void idle_state_handle(void){
     nrf_pwr_mgmt_run();
}



int main(void){
    timers_init();
    leds_init();
    power_management_init();
    ble_stack_init();
    advertising_init();

    advertising_start();

    bsp_board_led_on(2);
    for (;; ){
        idle_state_handle();
    }
}

