## NES260 - NES emulator for Xilinx KV260 FPGA board

This is a port of [fpganes](https://github.com/strigeus/fpganes) to the KV260 FPGA board.

<img src="doc/nes260_setup.jpg" width="300">

Current status:
* Most of the small games works (<64K), like Super Mario Bros, Adventure Island, Gradius, Battle City.
* Video works well through HDMI.
* Audio is done through a separate PMod module (IceSugar Audio).
* Game loading and controller is handled through a python GUI on PC.

### Running NES260

- Open Vivado 2022.1 and run the fpga\setup_project.tcl script
   - Click on Tools &rarr; Run Tcl Script... &rarr; <project_location>\fpga\setup_project.tcl
- Compile the Vivado project
- generate the XSA file
- open Vitis and create a new platform using the previous XSA file
- create a new application project and import all the sources from "sw" directory
- build
- open XSCT
- run those commands
- - connect
- - targets -set -nocase -filter {name =~ "\*PSU\*"}
- - mwr 0xff5e0200 0x0100
- - rst -system
- run app


If you see a grey screen after boot, then NES260 is ready for loading .nes ROMs. Connect KV260 to PC with USB cable and run `pc/nes26.py` with python to load games (`pip install pyserial itertools inputs kaitaistruct importlib`, then `python nes26.py`). USB game controller should be connected to the PC (**not** KV260). My Xbox 360 controllers work fine.

To get audio, connect a [Common audio amplifier](https://www.amazon.it/gp/product/B07DJ4NJXR/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1) module to the PMOD port (1-2 pins for the L-R channels, 5 to GROUND).

### Interested in retro-gaming or learning FPGA programming?

You can,

* Read my notes on some [technical details](doc/design.md) on how NES260 works, and compile/build the project yourself. The required Xilinx tools are free.
* Get the KV260 board. KV260 is currently available from Xilinx at [\$199](https://www.xilinx.com/products/som/kria/kv260-vision-starter-kit.html). It is not cheap. But it is a powerful board with basically a Xilinx Ultrascale+ ZU5EV SoC. Similar boards sell for twice the price or more. You can learn a lot with it if you have programming experience.
* Check out the most mature FPGA gaming project [Mister](https://misterfpga.org/). You can find many Youtube [videos](https://www.youtube.com/watch?v=rhT6YYRH1EI&t=8762s) on FPGA gaming. Mister supports a ton of consoles from Atari all the way to Playstation 1.
* Why make NES260 when there's already Mister? Actually Xilinx KV260 is much more powerful than the board Mister uses (Intel DE10-nano), and at roughly the same price. So it has potential for FPGA retro-gaming. The board was just released in 2021 and I haven't seen an emulator built with it. So here it goes.
* Also check out another FPGA project of mine, [neoapple2](https://github.com/zf3/neoapple2).

### Video demo

[![NES260 demo](https://img.youtube.com/vi/p09k8FfFO0Q/0.jpg)](https://www.youtube.com/watch?v=p09k8FfFO0Q)

MakarenaLabs , 04-2023