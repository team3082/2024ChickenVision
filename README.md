# 2024 Chicken Vision

## Web server setup


## Dependencies

* flask
* numpy
* opencv-contrib-python
* [apriltag](https://github.com/swatbotics/apriltag)

> [!IMPORTANT]
> As of commit https://github.com/team3082/2024ChickenVision/commit/79ceb6d822f879e656791f6bb5bb9a2b61418d66 the apriltag dependency is included in the codebase and the following block is nolonger required

<details>
<summary>Legacy Apriltag Lib setup</summary>

### apriltag lib setup

Because the original apriltag libary is unmaintianed we use the fork linked above. This fork can not be directly installed with pip and must be built from source.

#### Linux build instructions

1. Download latest source from [here](https://github.com/swatbotics/apriltag/archive/refs/heads/master.zip)
2. Extract the file and open the extracted folder in a terminal
3. Run $-`mkdir build && cd build`
4. Run $-`cmake .. -DCMAKE_BUILD_TYPE=Release`
5. Run $-`make -j4`
6. Run $-`sudo make install`
7. cd back to your ChickenVision folder then run `pip install apriltag`

</details>
