###############################################################
## NES260 - NES emulator for Xilinx KV260 FPGA board
## Vivado project generation script
## RPKH, 2023
###############################################################
set project_name "NES_KV260"

set part_name "xck26-sfvc784-2LV-c"
set board_name "xilinx.com:kv260_som:part0:1.3"
set board_connections "som240_1_connector xilinx.com:kv260_carrier:som240_1_connector:1.3"

set toplevel_name "bd_ipi_wrapper"
set toplevel_sim_name "test_nes"

set project_dir [file dirname [file normalize [info script]]]

set constr_dir [file join $project_dir constraints]
set rtl_dir [file join $project_dir rtl]
set sim_dir [file join $project_dir sim]
set vivado_dir [file join $project_dir vivado]

set bd_script [file join $project_dir bd_ipi.tcl]
set bd_name "bd_ipi"

file mkdir $vivado_dir
create_project $project_name $vivado_dir -part $part_name

if {$board_name != ""} {
    set_property board_part $board_name [current_project]

    if {$board_connections != ""} {
        set_property board_connections $board_connections [current_project]
    }
}

if {[get_filesets -quiet constrs_1] == ""} {
    create_fileset -constrset constrs_1
}
if {[file isdirectory $constr_dir] == 1} {
    add_files -fileset constrs_1 -quiet $constr_dir
}

if {[get_filesets -quiet sources_1] == ""} {
    create_fileset -srcset sources_1
}
if {[file isdirectory $rtl_dir] == 1} {
    add_files -fileset sources_1 -quiet $rtl_dir
}

# Xilinx's UNISIM library already has the module definitions defined in compat.v
# Disable the file to fix the "overwriting previous definition of module xx" critical warnings.
set_property is_enabled false [get_files -of_objects [get_filesets sources_1] compat.v]

if {[get_filesets -quiet sim_1] == ""} {
    create_fileset -simset sim_1
}
if {[file isdirectory $rtl_dir] == 1} {
    add_files -fileset sim_1 -quiet $sim_dir
}

if {$bd_script != ""} {
    source -quiet $bd_script
    regenerate_bd_layout

    make_wrapper -files [get_files [file join $vivado_dir ${project_name}.srcs sources_1 bd $bd_name ${bd_name}.bd]] -top
    add_files -norecurse [file join $vivado_dir ${project_name}.gen sources_1 bd $bd_name hdl ${bd_name}_wrapper.v]
}

if {$toplevel_name != ""} {
    set_property top $toplevel_name [get_filesets sources_1]
}

if {$toplevel_sim_name != ""} {
    set_property top $toplevel_sim_name [get_filesets sim_1]
}

update_compile_order -fileset sources_1
update_compile_order -fileset sim_1