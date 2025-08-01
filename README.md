# Tracking Task Progress with a Proactive Video Recording System

<img loop src="teaser.gif" width="100%"/>

## Abstract
Reliving past events is a crucial aspect of visual research, enabling deeper insights into both the sequence and context of actions. Ideally, a continuous recording would ensure that no moment is lost; however, this approach quickly becomes impractical due to the immense effort required to review and analyze large amounts of footage. To address this challenge, prior work has introduced devices equipped with sensors and cameras that automatically trigger recordings when predefined conditions are met. While this selective recording approach reduces unnecessary footage, it is limited to capturing only the present and lacks retrospective context, which is essential for analyzing complex scenarios. We introduce ChronoVault, an open-source framework designed for simple setup, configuration, and recording of retrospective videos. ChronoVault continuously monitors hardware- and software-signals, buffering a video-stream and saving said buffer, when specific conditions are detected. The system is built on the Raspberry Pi Zero 2, which supports camera integration and connectivity with peripheral devices. To evaluate ChronoVault we performed a user study. In it, participants were tasked to build a model out of building blocks and document the ends of certain subassembly tasks. Compared to an external reference camera, we reduce the footage amount, while retaining all relevant events.

## Material for reproducing/ appropriation
n the Work folder, you will find the code, 3D files for the case, and electronic schematics. Additionally, we provide an image of the entire operating system (OS) we used, which can be downloaded from [this link](https://uni-siegen.sciebo.de/s/Z9NccgHyLzWSwr3). The OS is configured to automatically launch into desktop mode.
The current username is "rpiPW123" and the password is "123". Please note: our software is deactivated in the OS image. To activate it, navigate to Desktop/ChronoVault/main.py and change line 126 to True.

## License
This project is licensed under the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/).

You are free to share and adapt the material, as long as you:
- Give appropriate credit  
- Do not use it for commercial purposes  
- Distribute any modified content under the same license  

## Contact
Michael Brilka (michael.brilka@uni-siegen.de)
