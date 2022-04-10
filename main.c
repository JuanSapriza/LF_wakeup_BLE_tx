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

#define ARRAY_LENGTH(array) (uint8_t)sizeof(array)

#define APP_BLE_CONN_CFG_TAG            1                                  /**< A tag identifying the SoftDevice BLE configuration. */

#define NON_CONNECTABLE_ADV_INTERVAL    MSEC_TO_UNITS(100, UNIT_0_625_MS)  /**< The advertising interval for non-connectable advertisement (100 ms). This value can vary between 100ms to 10.24s). */
#define NON_CONNECTABLE_ADV_TIMEOUT     MSEC_TO_UNITS(2000, UNIT_10_MS)

#define APP_AD_LEN_FLAG     ARRAY_LENGTH(((uint8_t[]){APP_AD_TYPE_FLAG,APP_AD_DATA_FLAG})) 
#define APP_AD_TYPE_FLAG    0X01
#define APP_AD_DATA_FLAG    0X06    // Nonconnectable, undirected 
#define APP_AD_LEN_MSD      ARRAY_LENGTH(((uint8_t[]){APP_AD_TYPE_MSD,APP_AD_DATA_MSD})) 
#define APP_AD_TYPE_MSD     0XFF
#define APP_AD_DATA_MSD     0X59,0x00  // Nordic Semiconductors
#define APP_AD_LEN_SHLN     ARRAY_LENGTH(((uint8_t[]){APP_AD_TYPE_SHLN,APP_AD_DATA_SHLN})) 
#define APP_AD_TYPE_SHLN    0x08    // Shortened Local Name   
#define APP_AD_DATA_SHLN    0x31,0x32,0x33,0x34,0x35,0x36,0x37,0x38,0x39,0x41,0x42,0X43,0X44,0x45  // ID on the Tag

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

static ble_gap_adv_data_t m_adv_data ={
    .adv_data =
    {
        .p_data = advData,
        .len    = BLE_GAP_ADV_SET_DATA_SIZE_MAX
    },
};


static void advertising_init(void){
    uint32_t      err_code;

    memset(&m_adv_params, 0, sizeof(m_adv_params));
    m_adv_params.properties.type = BLE_GAP_ADV_TYPE_NONCONNECTABLE_NONSCANNABLE_UNDIRECTED;
    m_adv_params.p_peer_addr     = NULL;    // Undirected advertisement.
    m_adv_params.filter_policy   = BLE_GAP_ADV_FP_ANY;
    m_adv_params.interval        = NON_CONNECTABLE_ADV_INTERVAL;
    m_adv_params.duration        = 300;      /**< Advertising duration in 10 ms units. When timeout is reached,
                                              an event of type @ref BLE_GAP_EVT_ADV_SET_TERMINATED is raised.
                                              @sa BLE_GAP_ADV_TIMEOUT_VALUES.
                                              @note The SoftDevice will always complete at least one advertising
                                              event even if the duration is set too low. */
    
    err_code = sd_ble_gap_adv_set_configure(&m_adv_handle, &m_adv_data, &m_adv_params);
    APP_ERROR_CHECK(err_code);

}


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

