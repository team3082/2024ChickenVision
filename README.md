# 2024 Chicken Vision

## Dependencies

* flask
* numpy
* robotpy-cscore
* opencv-contrib-python
* [apriltag](https://github.com/swatbotics/apriltag)

### apriltag lib setup

> 📝 **Notice:** It is planned to include this libary in future versions

Because the original apriltag libary is unmaintianed we use the fork linked above. This fork can not be directly installed with pip and must be built from source.

#### Linux build instructions

1. Download latest source from [here](https://github.com/swatbotics/apriltag/archive/refs/heads/master.zip)
2. Extract the file and open the extracted folder in a terminal
3. Run $-`mkdir build && cd build`
4. Run $-`cmake .. -DCMAKE_BUILD_TYPE=Release`
5. Run $-`make -j4`
6. Run $-`sudo make install`
7. cd back to your ChickenVision folder then run `pip install apriltag`
