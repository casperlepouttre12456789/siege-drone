A siege recon drone that uses a pi3a+ and a usbA camera and 2 360° servos and a power bank to do everything.
(no I haven't found a way to make it jump without using explosives)
<img src="blob:chrome-untrusted://media-app/5630590d-6904-46b3-ba16-cf829bde0f51" alt="1000034443.jpg"/><img width="4000" height="1800" alt="image" src="https://github.com/user-attachments/assets/9aee908d-24d3-4d11-be63-13eab6aa990a" />

tutorial: 3d print all the parts in petg or pla and the wheels in tpu (I used 95 but anything between 95 and 85 will work) then glue the 2 halves of the cilinder together using 5 second glue and put the servos through the wheel hubs and then attach you're crosses onto the servo using a screw and then glue the cross onto the wheel using hot glue (use a lot)
After that you want to flash the software and install all the requirements on the pi (I used ssh for this) then you can just glue on the camera and finish the wiring as instructed below and it should work.

wiring:
32 to Left servo signal
33 to Right servo signal
6	to Servo GND
2 to servo plus

Then you can use the drone by ssh to the drone then cd ~/siege-drone then source venv/bin/activate and then python app.py and then open your browser and enter this http://youre pi's ip adress:5000 
