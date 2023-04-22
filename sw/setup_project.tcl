###############################################################
## NES260 - NES emulator for Xilinx KV260 FPGA board
## Vitis project generation script
## RPKH, 2023
###############################################################
set platform_name "nes_kv260_platform"
set app_name "nes_kv260_app"

set project_dir [file dirname [file normalize [info script]]]
set src_dir [file join $project_dir src]
set vitis_dir [file join $project_dir vitis]
set xsa_file [file join $project_dir .. bin nes_kv260.xsa]

cd $project_dir

setws $vitis_dir

platform create -name $platform_name -hw $xsa_file -proc {psu_cortexa53_0} -os {standalone} -arch {64-bit} -fsbl-target {psu_cortexa53_0}

app create -name $app_name -platform $platform_name -proc psu_cortexa53_0 -os standalone -template "Empty Application(C)"
importsources -name $app_name -path $src_dir -soft-link

exit