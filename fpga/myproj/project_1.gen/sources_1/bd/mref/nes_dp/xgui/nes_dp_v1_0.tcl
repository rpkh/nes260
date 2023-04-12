# Definitional proc to organize widgets for parameters.
proc init_gui { IPINST } {
  ipgui::add_param $IPINST -name "Component_Name"
  #Adding Page
  set Page_0 [ipgui::add_page $IPINST -name "Page 0"]
  ipgui::add_param $IPINST -name "HA_END" -parent ${Page_0}
  ipgui::add_param $IPINST -name "HS_END" -parent ${Page_0}
  ipgui::add_param $IPINST -name "HS_STA" -parent ${Page_0}
  ipgui::add_param $IPINST -name "LINE" -parent ${Page_0}
  ipgui::add_param $IPINST -name "SCREEN" -parent ${Page_0}
  ipgui::add_param $IPINST -name "VA_END" -parent ${Page_0}
  ipgui::add_param $IPINST -name "VS_END" -parent ${Page_0}
  ipgui::add_param $IPINST -name "VS_STA" -parent ${Page_0}


}

proc update_PARAM_VALUE.HA_END { PARAM_VALUE.HA_END } {
	# Procedure called to update HA_END when any of the dependent parameters in the arguments change
}

proc validate_PARAM_VALUE.HA_END { PARAM_VALUE.HA_END } {
	# Procedure called to validate HA_END
	return true
}

proc update_PARAM_VALUE.HS_END { PARAM_VALUE.HS_END } {
	# Procedure called to update HS_END when any of the dependent parameters in the arguments change
}

proc validate_PARAM_VALUE.HS_END { PARAM_VALUE.HS_END } {
	# Procedure called to validate HS_END
	return true
}

proc update_PARAM_VALUE.HS_STA { PARAM_VALUE.HS_STA } {
	# Procedure called to update HS_STA when any of the dependent parameters in the arguments change
}

proc validate_PARAM_VALUE.HS_STA { PARAM_VALUE.HS_STA } {
	# Procedure called to validate HS_STA
	return true
}

proc update_PARAM_VALUE.LINE { PARAM_VALUE.LINE } {
	# Procedure called to update LINE when any of the dependent parameters in the arguments change
}

proc validate_PARAM_VALUE.LINE { PARAM_VALUE.LINE } {
	# Procedure called to validate LINE
	return true
}

proc update_PARAM_VALUE.SCREEN { PARAM_VALUE.SCREEN } {
	# Procedure called to update SCREEN when any of the dependent parameters in the arguments change
}

proc validate_PARAM_VALUE.SCREEN { PARAM_VALUE.SCREEN } {
	# Procedure called to validate SCREEN
	return true
}

proc update_PARAM_VALUE.VA_END { PARAM_VALUE.VA_END } {
	# Procedure called to update VA_END when any of the dependent parameters in the arguments change
}

proc validate_PARAM_VALUE.VA_END { PARAM_VALUE.VA_END } {
	# Procedure called to validate VA_END
	return true
}

proc update_PARAM_VALUE.VS_END { PARAM_VALUE.VS_END } {
	# Procedure called to update VS_END when any of the dependent parameters in the arguments change
}

proc validate_PARAM_VALUE.VS_END { PARAM_VALUE.VS_END } {
	# Procedure called to validate VS_END
	return true
}

proc update_PARAM_VALUE.VS_STA { PARAM_VALUE.VS_STA } {
	# Procedure called to update VS_STA when any of the dependent parameters in the arguments change
}

proc validate_PARAM_VALUE.VS_STA { PARAM_VALUE.VS_STA } {
	# Procedure called to validate VS_STA
	return true
}


proc update_MODELPARAM_VALUE.HA_END { MODELPARAM_VALUE.HA_END PARAM_VALUE.HA_END } {
	# Procedure called to set VHDL generic/Verilog parameter value(s) based on TCL parameter value
	set_property value [get_property value ${PARAM_VALUE.HA_END}] ${MODELPARAM_VALUE.HA_END}
}

proc update_MODELPARAM_VALUE.HS_STA { MODELPARAM_VALUE.HS_STA PARAM_VALUE.HS_STA } {
	# Procedure called to set VHDL generic/Verilog parameter value(s) based on TCL parameter value
	set_property value [get_property value ${PARAM_VALUE.HS_STA}] ${MODELPARAM_VALUE.HS_STA}
}

proc update_MODELPARAM_VALUE.HS_END { MODELPARAM_VALUE.HS_END PARAM_VALUE.HS_END } {
	# Procedure called to set VHDL generic/Verilog parameter value(s) based on TCL parameter value
	set_property value [get_property value ${PARAM_VALUE.HS_END}] ${MODELPARAM_VALUE.HS_END}
}

proc update_MODELPARAM_VALUE.LINE { MODELPARAM_VALUE.LINE PARAM_VALUE.LINE } {
	# Procedure called to set VHDL generic/Verilog parameter value(s) based on TCL parameter value
	set_property value [get_property value ${PARAM_VALUE.LINE}] ${MODELPARAM_VALUE.LINE}
}

proc update_MODELPARAM_VALUE.VA_END { MODELPARAM_VALUE.VA_END PARAM_VALUE.VA_END } {
	# Procedure called to set VHDL generic/Verilog parameter value(s) based on TCL parameter value
	set_property value [get_property value ${PARAM_VALUE.VA_END}] ${MODELPARAM_VALUE.VA_END}
}

proc update_MODELPARAM_VALUE.VS_STA { MODELPARAM_VALUE.VS_STA PARAM_VALUE.VS_STA } {
	# Procedure called to set VHDL generic/Verilog parameter value(s) based on TCL parameter value
	set_property value [get_property value ${PARAM_VALUE.VS_STA}] ${MODELPARAM_VALUE.VS_STA}
}

proc update_MODELPARAM_VALUE.VS_END { MODELPARAM_VALUE.VS_END PARAM_VALUE.VS_END } {
	# Procedure called to set VHDL generic/Verilog parameter value(s) based on TCL parameter value
	set_property value [get_property value ${PARAM_VALUE.VS_END}] ${MODELPARAM_VALUE.VS_END}
}

proc update_MODELPARAM_VALUE.SCREEN { MODELPARAM_VALUE.SCREEN PARAM_VALUE.SCREEN } {
	# Procedure called to set VHDL generic/Verilog parameter value(s) based on TCL parameter value
	set_property value [get_property value ${PARAM_VALUE.SCREEN}] ${MODELPARAM_VALUE.SCREEN}
}

