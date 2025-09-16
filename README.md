# Horatio-Ai-UW-Autonomous-Perception-Challenge


---
## Preface 

Although I've use python before, I've never worked with .npz files, pandas, or numpy, so my main goal was to simply write code that would output anything legible. On that note, I was succesful. In gereral, I relied heavily on ChatGPT to help with library syntax, but I made it a mission to have every line be written by me, which I also was succesful with.

---
## Method
I understood that the 4 parts of Part A were 
- 1: Read the RGB data in the csv
- 2: Pull the correlatin data from the npz file
- 3: Redefine the coordinate plane
- 4: Plot it
  
I decided to just be able to do part 1 and 2 as one method as they went along hand in hand, and I put away part 3 originally. Thus, the first iteration of my readData() function had no worldFrameReference or x/y axis definitions, and I simply printed all the x and y values I got from the npz files straight in the terminal. I quickly realized that I needed to disregard certain values (0's, NaN, and Inf), and once the coordinates I printed looked reasonable, I finished part 4. For part 3, ChatGPT is obsessed with tracking yaw throughout the entire series of frames to localize the EGO to the traffic light. I thought this was unnecesary, so to set the new coordinate plane I simply defined the vector between the EGO and traffic light in frame 1 as the x-axis, and for every subsequent point I used the vector projection formula to find the new x and y value.

---
## Assumptions
I assumed the sample output given had mixed up X and Y axises so I swapped them around for my output

---
## Results
The data I get from my npz files is incredibly jumpy along the y axis, and both the starting and ending coordinates are unreasonably large which makes my worlds bound far bigger than the example given. I couldnt solve either of these issues, and I assume that I have a fundamental misunderstanding on how npz files work, and how I am processing the data. However, my graph still gives a reasonable trajectory for the EGO within the frame of motion, although its frames as a sin curve as opposed to a parabola, so I assume the creation of my points, however flawed, is at least consistent. I assume the problems may have to do with my disregardment for the z-axis, or me projecting each frames magnitude onto the respective world frames axises rather than tracking the EGO's yaw relative to the traffic light to adjust for the car-centric coordinates given by the nps files, although I firmly believe that the projection method I use should be fine and yaw-independent.
