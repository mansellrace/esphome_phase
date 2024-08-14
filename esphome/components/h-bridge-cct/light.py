import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import light, output
from esphome.const import (
    CONF_OUTPUT_ID,
    CONF_COLD_WHITE,
    CONF_WARM_WHITE,
    CONF_COLD_WHITE_COLOR_TEMPERATURE,
    CONF_WARM_WHITE_COLOR_TEMPERATURE,
)

CODEOWNERS = ["@mansellrace"]

CONF_OVERLAP = "overlap"

h_bridge_cct_ns = cg.esphome_ns.namespace("h_bridge_cct")
HBridgeCCTLightOutput = h_bridge_cct_ns.class_("HBridgeCCTLightOutput", light.LightOutput)

CONFIG_SCHEMA = cv.All(
    light.RGB_LIGHT_SCHEMA.extend(
        {
            cv.GenerateID(CONF_OUTPUT_ID): cv.declare_id(HBridgeCCTLightOutput),
            cv.Required(CONF_COLD_WHITE): cv.use_id(output.FloatOutput),
            cv.Required(CONF_WARM_WHITE): cv.use_id(output.FloatOutput),
            cv.Optional(CONF_COLD_WHITE_COLOR_TEMPERATURE): cv.color_temperature,
            cv.Optional(CONF_WARM_WHITE_COLOR_TEMPERATURE): cv.color_temperature,
            cv.Optional(CONF_OVERLAP, default = "5%"): cv.templatable(cv.percentage),
        }
    ),
    cv.has_none_or_all_keys(
        [CONF_COLD_WHITE_COLOR_TEMPERATURE, CONF_WARM_WHITE_COLOR_TEMPERATURE]
    ),
    light.validate_color_temperature_channels,
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_OUTPUT_ID])
    await light.register_light(var, config)

    cwhite = await cg.get_variable(config[CONF_COLD_WHITE])
    cg.add(var.set_cold_white(cwhite))
    if cold_white_color_temperature := config.get(CONF_COLD_WHITE_COLOR_TEMPERATURE):
        cg.add(var.set_cold_white_temperature(cold_white_color_temperature))

    wwhite = await cg.get_variable(config[CONF_WARM_WHITE])
    cg.add(var.set_warm_white(wwhite))
    if warm_white_color_temperature := config.get(CONF_WARM_WHITE_COLOR_TEMPERATURE):
        cg.add(var.set_warm_white_temperature(warm_white_color_temperature))

    cg.add(var.set_overlap(config[CONF_OVERLAP]))