Works the same as the matrix prompt in automatic1111
Use a loop node such as the one found in easy-use to generate the images

How to use:
Works the same way as automatic1111 prompt matrix
https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/features#prompt-matrix
1girl, prompt, goes, here, first, |masterpiece|high quality|newest

- STRING
  - returns the different combinations, including the "main prompt"
- STRING_minus_main_prompt
  - returns the tokens after the first | (removes "1girl, prompt, goes, here, first,") use this for labels
- length
  - returns the number of images that will be generated
- column_count
  - returns column count, use it for a grid
- row_count
  - returns row count, use it for a grid
![image](https://github.com/user-attachments/assets/b73d01fb-bf46-417b-ae35-f7c4157f78cc)

You can find it under "utils"
![image](https://github.com/user-attachments/assets/896c66ac-1735-4dbd-b424-62bf921529ec)



