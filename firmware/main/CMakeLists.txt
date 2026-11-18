idf_component_register(SRCS "signalbench.c" "sniff_core.c"
  INCLUDE_DIRS "."
  REQUIRES esp_adc driver esp_timer esp_hw_support esp_system json)
