#pragma once

#include "esphome/components/light/light_output.h"
#include "esphome/components/output/float_output.h"
#include "esphome/core/component.h"

namespace esphome {
namespace h_bridge_cct {

class HBridgeCCTLightOutput : public light::LightOutput {
 public:
  void set_cold_white(output::FloatOutput *cold_white) { cold_white_ = cold_white; }
  void set_warm_white(output::FloatOutput *warm_white) { warm_white_ = warm_white; }
  void set_cold_white_temperature(float cold_white_temperature) { cold_white_temperature_ = cold_white_temperature; }
  void set_warm_white_temperature(float warm_white_temperature) { warm_white_temperature_ = warm_white_temperature; }
  void set_overlap(float overlap) { overlap_ = overlap / 2; }
  light::LightTraits get_traits() override {
    auto traits = light::LightTraits();
    traits.set_supported_color_modes({light::ColorMode::COLOR_TEMPERATURE});
    traits.set_min_mireds(this->cold_white_temperature_);
    traits.set_max_mireds(this->warm_white_temperature_);
    return traits;
  }
  void write_state(light::LightState *state) override {
    float cwhite, wwhite, phase;
    float color_temperature, brightness;
    state->current_values_as_ct(&color_temperature, &brightness);
    cwhite = brightness * color_temperature;
    wwhite = brightness - cwhite;
    phase = ((1.0 - cwhite - wwhite) * 180.0) + cwhite * 360.0;
    this->warm_white_->update_phase_angle(phase);
    if (color_temperature > 0 && color_temperature < 1.0) {
      cwhite -= this->overlap_;
      wwhite -= this->overlap_;
    }
    this->cold_white_->set_level(cwhite);
    this->warm_white_->set_level(wwhite);
  }

 protected:
  output::FloatOutput *cold_white_;
  output::FloatOutput *warm_white_;
  float cold_white_temperature_{0};
  float warm_white_temperature_{0};
  float overlap_;
};

}  // namespace h_bridge_cct
}  // namespace esphome