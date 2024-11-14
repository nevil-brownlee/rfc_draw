
rdd objects table:

| type   | key, coords,  text  |  parent_id  |   v1    |     v2    |
| ------ | ------------------- | ----------- | ------- | --------- | 
| header |    ,       ,   "H"  | top line id | hdr nbr |     0     |
| row    |    ,       ,   "R"  | hdr id      | row nbr |  n_lines  |
| field  |    ,       , f_text | row id      | f_col   |   width   |
!        |                     |             |         |           |
! n_rect |    ,       , nr_ext | -           |         |    0      |
| line   |    ,       , l_opt  | 0           | N?      |    0      |
| text   |    ,       ,        | 0           | 0       |    A?     |
| ------ | ------------------- | ----------- | ------- | --------- | 


l_opt:  a for arrow, n for no arrrows
        e syntax end markers, b no end markers (bare)
N?:     N in rdd v1,   0 in v2
A?      "0" in rdd v1, 0 in v2