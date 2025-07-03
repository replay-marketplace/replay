### Compute Operations
#### Compute APIs

  * [copy_tile](copy_tile.html)
  * [move_copy_tile](move_copy_tile.html)
  * [acquire_dst](acquire_dst.html)
  * [release_dst](release_dst.html)
  * [reg_api](reg_api.html)
  * [any_init](init_functions.html)
  * [abs_tile](abs_tile.html)
  * [add_tiles](add_tiles.html)
  * [sub_tiles](sub_tiles.html)
  * [mul_tiles](mul_tiles.html)
  * [add_tiles_bcast](add_tiles_bcast.html)
  * [sub_tiles_bcast](sub_tiles_bcast.html)
  * [mul_tiles_bcast](mul_tiles_bcast.html)
  * [matmul_tiles](matmul_tiles.html)
  * [matmul_block](matmul_block.html)
  * [exp_tile](exp_tile.html)
  * [exp2_tile](exp2_tile.html)
  * [expm1_tile](expm1_tile.html)
  * [relu_tile](relu_tile.html)
  * [relu_max_tile](relu_tile.html#relu-max-tile)
  * [relu_min_tile](relu_tile.html#relu-min-tile)
  * [leaky_relu_tile](relu_tile.html#leaky-relu-tile)
  * [elu_tile](elu_tile.html)
  * [erf_tile](erf_tile.html)
  * [erfc_tile](erfc_tile.html)
  * [erfinv_tile](erfinv_tile.html)
  * [gelu_tile](gelu_tile.html)
  * [heaviside_tile](heaviside_tile.html)
  * [isinf_tile](isinf_tile.html)
  * [isposinf_tile](isinf_tile.html#isposinf-tile)
  * [isneginf_tile](isinf_tile.html#isneginf-tile)
  * [isfinite_tile](isinf_tile.html#isfinite-tile)
  * [isnan_tile](isnan_tile.html)
  * [i0_tile](i0_tile.html)
  * [logical_not_unary_tile](logical_not_unary_tile.html)
  * [recip_tile](recip_tile.html)
  * [sign_tile](sign_tile.html)
  * [sqrt_tile](sqrt_tile.html)
  * [rsqrt_tile](rsqrt_tile.html)
  * [sigmoid_tile](sigmoid_tile.html)
  * [log_tile](log_tile.html)
  * [log_with_base_tile](log_with_base_tile.html)
  * [power_tile](power_tile.html)
  * [rsub_tile](rsub_tile.html)
  * [signbit_tile](signbit_tile.html)
  * [square_tile](square_tile.html)
  * [reduce_tile](reduce_tile.html)
  * [transpose_wh_tile](transpose_wh_tile.html)
  * [tanh_tile](tanh_tile.html)
  * [tan_tile](tan_tile.html)
  * [sin_tile](sin_tile.html)
  * [cos_tile](cos_tile.html)
  * [asin_tile](asin_tile.html)
  * [atan_tile](atan_tile.html)
  * [acos_tile](acos_tile.html)
  * [ltz_tile](ltz_tile.html)
  * [eqz_tile](eqz_tile.html)
  * [lez_tile](lez_tile.html)
  * [gtz_tile](gtz_tile.html)
  * [gez_tile](gez_tile.html)
  * [nez_tile](nez_tile.html)
  * [unary_ne_tile](unary_ne_tile.html)
  * [unary_gt_tile](unary_gt_tile.html)
  * [unary_lt_tile](unary_lt_tile.html)
  * [cb_wait_front](cb_wait_front.html)
  * [cb_pop_front](cb_pop_front.html)
  * [cb_reserve_back](cb_reserve_back.html)
  * [cb_push_back](cb_push_back.html)
  * [binary_init_funcs](binary_op_init_funcs.html)
  * [tilize](tilize.html)
  * [untilize](untilize.html)

#### atan_tile

void ckernel::atan_tile_init()  

Please refer to documentation for any_init.

void ckernel::atan_tile(uint32_t idst)      

Performs element-wise computation of arctan on each element of a tile in DST
register at index tile_index. The DST register buffer must be in acquired
state via _acquire_dst_ call. This call is blocking and is only available on
the compute engine.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
idst  | The index of the tile in DST register buffer to perform the computation on  | uint32_t  | Must be less than the size of the DST register buffer  | True 

#### matmul_tiles

void ckernel::mm_init(uint32_t in0_cb_id, uint32_t in1_cb_id, uint32_t
out_cb_id, const uint32_t transpose = 0)  

Initialization for matmul_tiles operation. Must be called before matmul_tiles.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
in0_cb_id  | The identifier of the first input circular buffer (CB)  | uint32_t  | 0 to 31  | False   
in1_cb_id  | The identifier of the second input circular buffer (CB)  | uint32_t  | 0 to 31  | False   
out_cb_id  | The identifier of the output circular buffer (CB)  | uint32_t  | 0 to 31  | False   
transpose  | The transpose flag for performing transpose operation on B  | uint32_t  | Any positive value will indicate tranpose is set  | False   
  
void ckernel::mm_init_short_with_dt(uint32_t in0_cb_id, uint32_t in1_cb_id,
uint32_t c_in_old_srca, const uint32_t transpose = 0)  

A short version of matmul_tiles initialization. It is used to reconfigure srcA
of the compute engine back to matmul mode.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
in0_cb_id  | The identifier of the first input circular buffer (CB)  | uint32_t  | 0 to 31  | False   
in1_cb_id  | The identifier of the second input circular buffer (CB)  | uint32_t  | 0 to 31  | False   
c_in_old_srca  | The identifier of the old input to src A circular buffer (CB)  | uint32_t  | 0 to 31  | False   
transpose  | The transpose flag for performing transpose operation on B  | uint32_t  | Any positive value will indicate tranpose is set  | False   
  
void ckernel::mm_init_short(uint32_t in0_cb_id, uint32_t in1_cb_id, const
uint32_t transpose = 0)  

A short version of matmul_tiles initialization. Configure the unpacker and
math engine to matmul mode.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
in0_cb_id  | The identifier of the first input circular buffer (CB)  | uint32_t  | 0 to 31  | False   
in1_cb_id  | The identifier of the second input circular buffer (CB)  | uint32_t  | 0 to 31  | False   
transpose  | The transpose flag for performing transpose operation on B  | uint32_t  | Any positive value will indicate tranpose is set  | False   
  
void ckernel::matmul_tiles(uint32_t in0_cb_id, uint32_t in1_cb_id, uint32_t
in0_tile_index, uint32_t in1_tile_index, uint32_t idst, const uint32_t
transpose)  

Performs tile-sized matrix multiplication _C=A*B_ between the tiles in two
specified input CBs and writes the result to DST. The DST register buffer must
be in acquired state via _acquire_dst_ call. This call is blocking and is only
available on the compute engine.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
in0_cb_id  | The identifier of the first input circular buffer (CB)  | uint32_t  | 0 to 31  | True   
in1_cb_id  | The identifier of the second input circular buffer (CB)  | uint32_t  | 0 to 31  | True   
in0_tile_index  | The index of the tile A from the first input CB  | uint32_t  | Must be less than the size of the CB  | True   
in1_tile_index  | The index of the tile B from the second input CB  | uint32_t  | Must be less than the size of the CB  | True   
dst_tile_index  | The index of the tile in DST REG to which the result C will be written.  | uint32_t  | Must be less than the acquired size of DST REG  | True 

#### copy_tile

void ckernel::copy_tile(uint32_t in_cb_id, uint32_t in_tile_index, uint32_t
dst_tile_index)  

Copies a single tile from the specified input CB and writes the result to DST
at a specified index. The function will employ unpacker to first unpack into
SRC registers and then perform move into DST registers, at a specified index.
For the in_tile_index to be valid for this call, cb_wait_front(n) had to be
previously called to ensure that at least some number n>0 of tiles are
available in the input CB. The CB index 0 then references the first tile in
the received section of the CB, up to index n-1 (in a FIFO order). The DST
register buffer must be in acquired state via acquire_dst call. This call is
blocking and is only available on the compute engine.

Return value: None

Argument  | Description  | Data type  | Valid range  | required   
---|---|---|---|---  
in_cb_id  | The identifier of the source circular buffer (CB)  | uint32_t  | 0 to 31  | True   
in_tile_index  | The index of the tile to copy from the input CB  | uint32_t  | Must be less than the size of the CB  | True   
dst_tile_index  | The index of the tile in the DST register  | uint32_t  | Must be less than the size of the DST register (16)  | True 

#### erfc_tile
template<bool fast_and_approx = true>  
void ckernel::erfc_tile_init()  

Please refer to documentation for any_init.

template<bool fast_and_approx = true>  
void ckernel::erfc_tile(uint32_t idst)  

Performs element-wise computation of complimentary error function on each
element of a tile in DST register at index tile_index. The DST register buffer
must be in acquired state via _acquire_dst_ call. This call is blocking and is
only available on the compute engine.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
tile_index  | The index of the tile in DST register buffer to perform the computation on  | uint32_t  | Must be less than the size of the DST register buffer  | True 

#### unary_lt_tile

void ckernel::unary_lt_tile_init()  

Please refer to documentation for any_init.

void ckernel::unary_lt_tile(uint32_t idst, uint32_t param0)  

Performs element-wise computation of: result = 1 if x < value , where x is
each element of a tile in DST register at index tile_index. The value is
provided as const param0 The DST register buffer must be in acquired state via
_acquire_dst_ call. This call is blocking and is only available on the compute
engine.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
idst  | The index of the tile in DST register buffer to perform the computation on  | uint32_t  | Must be less than the size of the DST register buffer  | True   
param0  | The value to be compared with the input tensor  | uint32_t  |  | True

#### log_with_base_tile

void ckernel::log_with_base_tile_init()  

Please refer to documentation for any_init.

void ckernel::log_with_base_tile(uint32_t idst, uint32_t base_scale)  

Performs element-wise computation of logarithm with a specified base on each
element of a tile in DST register at index tile_index. The DST register buffer
must be in acquired state via _acquire_dst_ call. This call is blocking and is
only available on the compute engine.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
idst  | The index of the tile in DST register buffer to perform the computation on  | uint32_t  | Must be less than the size of the DST register buffer  | True   
base_scale  | The log base  | uint32_t  | Postive integers  | True

#### mul_tiles_bcast

void ckernel::mul_bcast_cols_init_short(uint32_t icb0, uint32_t icb1)  

Performs a first-call or switch-from-another-op tile hw reconfiguration step
needed for mul_bcast_cols to be executed correctly.

void ckernel::mul_bcast_rows_init_short(uint32_t icb0, uint32_t icb1)  

Performs a switch-from-another-op tile hw reconfiguration step needed for
mul_bcast_rows to be executed correctly.

template<BroadcastType tBcastDim>  
void ckernel::mul_tiles_bcast(uint32_t icb0, uint32_t icb1, uint32_t itile0,
uint32_t itile1, uint32_t idst)  

Please refer to documentation for _add_tiles_bcast_.

void ckernel::mul_tiles_bcast_scalar_init_short(uint32_t icb0, uint32_t icb1)  

Performs a first-call or switch-from-another-op tile hw reconfiguration step
needed for mul_bcast_cols to be executed correctly.

void ckernel::mul_tiles_bcast_scalar(uint32_t icb0, uint32_t icb1, uint32_t
itile0, uint32_t itile1, uint32_t idst)  

Performs a broadcast-multiply of a tile from icb0[itile0] with a scalar
encoded as a tile from icb1[itile1].

#### cos_tile

void ckernel::cos_tile_init()  

Please refer to documentation for any_init.

void ckernel::cos_tile(uint32_t idst)  

Performs element-wise computation of the trigonometric cosine operation on
each element of a tile in DST register at index tile_index. The DST register
buffer must be in acquired state via _acquire_dst_ call. This call is blocking
and is only available on the compute engine.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
tile_index  | The index of the tile in DST register buffer to perform the computation on  | uint32_t  | Must be less than the size of the DST register buffer  | True

#### eqz_tile

void ckernel::eqz_tile_init()  

Please refer to documentation for any_init.

void ckernel::eqz_tile(uint32_t idst)  

Will store in the output of the compute core True if each element of a equal
to zero. The DST register buffer must be in acquired state via _acquire_dst_
call. This call is blocking and is only available on the compute engine.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
idst  | The index of the tile in DST register buffer to perform the computation on  | uint32_t  | Must be less than the size of the DST register buffer  | True

#### unary_gt_tile

void ckernel::unary_gt_tile_init()  

Please refer to documentation for any_init.

void ckernel::unary_gt_tile(uint32_t idst, uint32_t param0)  

Performs element-wise computation of: result = 1 if x > value , where x is
each element of a tile in DST register at index tile_index. The value is
provided as const param0 The DST register buffer must be in acquired state via
_acquire_dst_ call. This call is blocking and is only available on the compute
engine.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
idst  | The index of the tile in DST register buffer to perform the computation on  | uint32_t  | Must be less than the size of the DST register buffer  | True   
param0  | The value to be compared with the input tensor  | uint32_t  |  | True

#### mul_tiles

void ckernel::mul_tiles_init_f()  

Please refer to documentation for any_init. f means high fidelity with
resepect to accuracy this is set during createprogram

void ckernel::mul_tiles_init(uint32_t icb0, uint32_t icb1)  

Please refer to documentation for any_init.

void ckernel::mul_tiles(uint32_t icb0, uint32_t icb1, uint32_t itile0,
uint32_t itile1, uint32_t idst)  

Performs element-wise multiplication C=A*B of tiles in two CBs at given
indices and writes the result to the DST register at index dst_tile_index. The
DST register buffer must be in acquired state via _acquire_dst_ call. This
call is blocking and is only available on the compute engine.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
in0_cb_id  | The identifier of the circular buffer (CB) containing A  | uint32_t  | 0 to 31  | True   
in1_cb_id  | The identifier of the circular buffer (CB) containing B  | uint32_t  | 0 to 31  | True   
in0_tile_index  | The index of tile A within the first CB  | uint32_t  | Must be less than the size of the CB  | True   
in1_tile_index  | The index of tile B within the second CB  | uint32_t  | Must be less than the size of the CB  | True   
dst_tile_index  | The index of the tile in DST REG for the result C  | uint32_t  | Must be less than the acquired size of DST REG  | True

#### nez_tile

void ckernel::nez_tile_init()  

Please refer to documentation for any_init.

void ckernel::nez_tile(uint32_t idst)  

Will store in the output of the compute core True if each element is not equal
to zero. The DST register buffer must be in acquired state via _acquire_dst_
call. This call is blocking and is only available on the compute engine.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
idst  | The index of the tile in DST register buffer to perform the computation on  | uint32_t  | Must be less than the size of the DST register buffer  | True

#### sign_tile

void ckernel::sign_tile_init()  

Please refer to documentation for any_init.

void ckernel::sign_tile(uint32_t idst)  

Will store in the output of the compute core the signum of the tile. The DST
register buffer must be in acquired state via _acquire_dst_ call. This call is
blocking and is only available on the compute engine.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
idst  | The index of the tile in DST register buffer to perform the computation on  | uint32_t  | Must be less than the size of the DST register buffer  | True

#### move_copy_tile

void ckernel::copy_tile_to_dst_init_short_with_dt(uint32_t old_cbid, uint32_t
new_cbid, uint32_t transpose = 0)  

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
old_cbid  | The identifier of the previous input circular buffer (CB) to SrcA  | uint32_t  | 0 to 31  | True   
new_cbid  | The identifier of the new input circular buffer (CB) to SrcA  | uint32_t  | 0 to 31  | True   
transpose  | Flag to perform transpose on SrcA  | uint32_t  | Any positive value will indicate tranpose is set  | False   
  
void ckernel::copy_tile_to_dst_init_short(uint32_t cbid, uint32_t transpose =
0)  

Perform the init short for copy tile. This does not reconfigure the unpacker
data types. Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
cbid  | The identifier of the input circular buffer (CB)  | uint32_t  | 0 to 31  | False   
transpose  | Flag to perform transpose on SrcA  | uint32_t  | Any positive value will indicate tranpose is set  | False   
  
void ckernel::copy_tile_init(uint32_t cbid)  

Perform a init for the copy tile operation. This calls the short init function
and initializes packer dst offset registers.
#### transpose_wh_tile

void ckernel::transpose_wh_init(uint32_t icb, uint32_t ocb)  

Paired Init function for transpose_wh. For general information on init
functions refer to any_init.

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
icb  | The identifier of the circular buffer (CB) containing input  | uint32_t  | 0 to 31  | True   
  
void ckernel::transpose_wh_tile(uint32_t icb, uint32_t itile, uint32_t idst)  

Performs a 32x32 transpose operation _B[w,h] = A[h,w]_ on a tile in the CB at
a given index and writes the result to the DST register at index
dst_tile_index. The DST register buffer must be in acquired state via
_acquire_dst_ call.

This call is blocking and is only available on the compute engine.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
in_cb_id  | The identifier of the circular buffer (CB) containing A  | uint32_t  | 0 to 31  | True   
in_tile_index  | The index of tile A within the first CB  | uint32_t  | Must be less than the size of the CB  | True   
dst_tile_index  | The index of the tile in DST REG for the result B  | uint32_t  | Must be less than the acquired size of DST REG  | True

#### elu_tile

void ckernel::elu_tile_init()  

Please refer to documentation for any_init.

void ckernel::elu_tile(uint32_t idst, uint32_t param0)  

Performs element-wise computation of elu (relu(x) + slope*(exp(x) - 1)*(x <= 0
)) on each element of a tile in DST register at index tile_index. The DST
register buffer must be in acquired state via _acquire_dst_ call. This call is
blocking and is only available on the compute engine.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
tile_index  | The index of the tile in DST register buffer to perform the computation on  | uint32_t  | Must be less than the size of the DST register buffer  | True   
slope  | slope used in elu calculation  | uint32_t  | Greater than 0  | True

#### isinf_tile

void ckernel::isinf_tile_init()  

Please refer to documentation for any_init.

void ckernel::isinf_tile(uint32_t idst)  

Will store in the output of the compute core True if the input tile is
infinity. The DST register buffer must be in acquired state via _acquire_dst_
call. This call is blocking and is only available on the compute engine.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
tile_index  | The index of the tile in DST register buffer to perform the computation on  | uint32_t  | Must be less than the size of the DST register buffer  | True   
  
# isposinf_tile

void ckernel::isposinf_tile_init()  

Please refer to documentation for any_init.

void ckernel::isposinf_tile(uint32_t idst)  

Will store in the output of the compute core True if the input tile is
positive infinity. The DST register buffer must be in acquired state via
_acquire_dst_ call. This call is blocking and is only available on the compute
engine.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
tile_index  | The index of the tile in DST register buffer to perform the computation on  | uint32_t  | Must be less than the size of the DST register buffer  | True   
  
# isneginf_tile

void ckernel::isneginf_tile_init()  

Please refer to documentation for any_init.

void ckernel::isneginf_tile(uint32_t idst)  

Will store in the output of the compute core True if the input tile is
negative infinity. The DST register buffer must be in acquired state via
_acquire_dst_ call. This call is blocking and is only available on the compute
engine.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
tile_index  | The index of the tile in DST register buffer to perform the computation on  | uint32_t  | Must be less than the size of the DST register buffer  | True   
  
# isfinite_tile

void ckernel::isfinite_tile_init()  

Please refer to documentation for any_init.

void ckernel::isfinite_tile(uint32_t idst)  

Will store in the output of the compute core True if the input tile is finite
The DST register buffer must be in acquired state via _acquire_dst_ call. This
call is blocking and is only available on the compute engine.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
tile_index  | The index of the tile in DST register buffer to perform the computation on  | uint32_t  | Must be less than the size of the DST register buffer  | True

#### relu_tile

void ckernel::relu_tile_init()  

Please refer to documentation for any_init.

void ckernel::relu_tile(uint32_t idst)  

Performs element-wise computation of relu (0 if negative else 1) on each
element of a tile in DST register at index tile_index. The DST register buffer
must be in acquired state via _acquire_dst_ call. This call is blocking and is
only available on the compute engine.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
tile_index  | The index of the tile in DST register buffer to perform the computation on  | uint32_t  | Must be less than the size of the DST register buffer  | True   
  
# relu_max_tile

void ckernel::relu_max_tile_init()  

Please refer to documentation for any_init.

void ckernel::relu_max_tile(uint32_t idst, uint32_t param0)  

Performs element-wise computation of relu max (relu(max(x, upper_limit))) on
each element of a tile in DST register at index tile_index. The DST register
buffer must be in acquired state via _acquire_dst_ call. This call is blocking
and is only available on the compute engine.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
tile_index  | The index of the tile in DST register buffer to perform the computation on  | uint32_t  | Must be less than the size of the DST register buffer  | True   
upper_limit  | Upper limit of relu_min  | uint32_t  | Greater than 0  | True   
  
# relu_min_tile

void ckernel::relu_min_tile_init()  

Please refer to documentation for any_init.

void ckernel::relu_min_tile(uint32_t idst, uint32_t param0)  

Performs element-wise computation of relu min (relu(min(x, lower_limit))) on
each element of a tile in DST register at index tile_index. The DST register
buffer must be in acquired state via _acquire_dst_ call. This call is blocking
and is only available on the compute engine.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
tile_index  | The index of the tile in DST register buffer to perform the computation on  | uint32_t  | Must be less than the size of the DST register buffer  | True   
lower_limit  | Upper limit of relu_min  | uint32_t  | Greater than 0  | True   
  
# leaky_relu_tile

void ckernel::leaky_relu_tile_init()  

Please refer to documentation for any_init.

void ckernel::leaky_relu_tile(uint32_t idst, uint32_t slope)  

Performs element-wise computation of leaky relu (relu(x) + slope*-relu(-x)) on
each element of a tile in DST register at index tile_index. The DST register
buffer must be in acquired state via _acquire_dst_ call. This call is blocking
and is only available on the compute engine.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
tile_index  | The index of the tile in DST register buffer to perform the computation on  | uint32_t  | Must be less than the size of the DST register buffer  | True   
slope  | slope used in leaky relu - will reinterpret unsigned int to float  | uint32_t  | Greater than 0  | True

#### untilize

void ckernel::untilize_init(uint32_t icb, uint32_t ocb)  

Init function for untilize operations, to be used at the beginning of the
kernel.

void ckernel::untilize_init_short(uint32_t icb)  

Short init function to initialize untilize op, after a full init is already
performed.

template<int N = 1>  
void ckernel::untilize_block(uint32_t icb, uint32_t block, uint32_t ocb)  

Perform the untilize operation on a block of tiles. This simply loops over the
provided block size.

void ckernel::untilize_uninit(uint32_t icb)  

Uninitialize untilize operation, to allow initializing another operation.

#### gtz_tile

void ckernel::gtz_tile_init()  

Please refer to documentation for any_init.

void ckernel::gtz_tile(uint32_t idst)  

Will store in the output of the compute core True if each element is greater
than zero. The DST register buffer must be in acquired state via _acquire_dst_
call. This call is blocking and is only available on the compute engine.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
idst  | The index of the tile in DST register buffer to perform the computation on  | uint32_t  | Must be less than the size of the DST register buffer  | True

#### power_tile

void ckernel::power_tile_init()  

Please refer to documentation for any_init.

void ckernel::power_tile(uint32_t idst, uint32_t param0)  

Performs element-wise computation of power operation (x ^(const param0)) value
on each element of a tile in DST register at index tile_index. The DST
register buffer must be in acquired state via _acquire_dst_ call. This call is
blocking and is only available on the compute engine.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
idst  | The index of the tile in DST register buffer to perform the computation on  | uint32_t  | Must be less than the size of the DST register buffer  | True   
param0  | The value of the exponent in the power operation  | uint32_t  |  | True

#### logical_not_unary_tile

void ckernel::logical_not_unary_tile_init()  

Please refer to documentation for any_init.

void ckernel::logical_not_unary_tile(uint32_t idst)  

Performs element-wise computation of the logical not unary operation on each
element of a tile in DST register at index tile_index. The DST register buffer
must be in acquired state via _acquire_dst_ call. This call is blocking and is
only available on the compute engine.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
tile_index  | The index of the tile in DST register buffer to perform the computation on  | uint32_t  | Must be less than the size of the DST register buffer  | True

#### heaviside_tile

void ckernel::heaviside_tile_init()  

Please refer to documentation for any_init.

void ckernel::heaviside_tile(uint32_t idst, uint32_t param0)  

Performs element-wise computation of: y = 0 if x < 0 , 1 if x > 0 , y= value
where x is each element of a tile in DST register at index tile_index. The
value is provided as const param0 The DST register buffer must be in acquired
state via _acquire_dst_ call. This call is blocking and is only available on
the compute engine.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
idst  | The index of the tile in DST register buffer to perform the computation on  | uint32_t  | Must be less than the size of the DST register buffer  | True   
param0  | The value the output is if the input is greater than 0  | uint32_t  |  | True

#### acos_tile

void ckernel::acos_tile_init()  

Please refer to documentation for any_init.

void ckernel::acos_tile(uint32_t idst)  

Performs element-wise computation of arccossine on each element of a tile in
DST register at index tile_index. The DST register buffer must be in acquired
state via _acquire_dst_ call. This call is blocking and is only available on
the compute engine.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
idst  | The index of the tile in DST register buffer to perform the computation on  | uint32_t  | Must be less than the size of the DST register buffer  | True

#### add_tiles_bcast

void ckernel::add_bcast_cols_init_short(uint32_t icb0, uint32_t icb1)  

Performs a first-call or switch-from-another-op tile hw reconfiguration step
needed for add_bcast_cols to be executed correctly. Required to be called
before add_tiles_bcast if using column as broadcast type

void ckernel::add_bcast_rows_init_short(uint32_t icb0, uint32_t icb1)  

Performs a first-call or switch-from-another-op tile hw reconfiguration step
needed for add_bcast_rows to be executed correctly. Required to be called
before add_tiles_bcast if using column as broadcast type

template<BroadcastType tBcastDim>  
void ckernel::add_tiles_bcast(uint32_t icb0, uint32_t icb1, uint32_t itile0,
uint32_t itile1, uint32_t idst)  

This documentation applies to either one of the 3 broadcast operation variants
- _add_tiles_bcast_ , _sub_tiles_bcast_ and _mul_tiles_bcast_.

The description below describes _add_tiles_bcast_ , the other 2 operations use
the same definition with the corresponding substitution of the math operator.

Performs a broadcast-operation _C=A+B_ of tiles in two CBs at given indices
and writes the result to the DST register at index dst_tile_index. The DST
register buffer must be in acquired state via _acquire_dst_ call. This call is
blocking and is only available on the compute engine.

Broadcasting semantics are defined as follows:

For _dim==BroadcastType::COL_ , the input in _B_ is expected to be a single
tile with a filled 0-column and zeros elsewhere. The result is _C[h, w] =
A[h,w] + B[w]_

For _dim==Dim::C_ , the input in _B_ is expected to be a single tile with a
filled 0-row, and zeros elsewhere. The result is _C[h, w] = A[h,w] + B[h]_

For _dim==Dim::RC_ , the input in _B_ is expected to be a single tile with a
filled single value at location [0,0], and zeros elsewhere. The result is
_C[h, w] = A[h,w] + B[0,0]_

Return value: None

DOX-TODO(AP): verify that the bcast tile is actually required to be filled
with zeros.

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
tBcastDim  | Broadcast dimension  | BroadcastType  | One of Dim::R, Dim::C, Dim::RC.  | True   
in0_cb_id  | The identifier of the circular buffer (CB) containing A  | uint32_t  | 0 to 31  | True   
in1_cb_id  | The indentifier of the circular buffer (CB) containing B  | uint32_t  | 0 to 31  | True   
in0_tile_index  | The index of tile A within the first CB  | uint32_t  | Must be less than the size of the CB  | True   
in1_tile_index  | The index of tile B within the second CB  | uint32_t  | Must be less than the size of the CB  | True   
dst_tile_index  | The index of the tile in DST REG for the result C  | uint32_t  | Must be less than the acquired size of DST REG  | True

#### tan_tile

void ckernel::tan_tile_init()  

Please refer to documentation for any_init.

void ckernel::tan_tile(uint32_t idst)  

Performs element-wise computation of the trigonometric tan operation on each
element of a tile in DST register at index tile_index. The DST register buffer
must be in acquired state via _acquire_dst_ call. This call is blocking and is
only available on the compute engine.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
tile_index  | The index of the tile in DST register buffer to perform the computation on  | uint32_t  | Must be less than the size of the DST register buffer  | True

#### ltz_tile

void ckernel::ltz_tile_init()  

Please refer to documentation for any_init.

void ckernel::ltz_tile(uint32_t idst)  

Will store in the output of the compute core True if each element of a tile is
less than zero. The DST register buffer must be in acquired state via
_acquire_dst_ call. This call is blocking and is only available on the compute
engine.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
idst  | The index of the tile in DST register buffer to perform the computation on  | uint32_t  | Must be less than the size of the DST register buffer  | True

#### release_dst

void ckernel::release_dst()  

_Deprecated:_

This function is deprecated, please use
`[tile_regs_release()](reg_api.html#namespaceckernel_1addd3679665da343bd51f76ced7154c4a)`
instead. See <https://github.com/tenstorrent/tt-
metal/issues/5868#issuecomment-2101726935>

Releases the exclusive lock on the internal DST register for the current
Tensix core. This lock had to be previously acquired with acquire_dst. This
call is blocking and is only available on the compute engine.

Return value: None

How the destination register will be shared and synchronized between TRISC
threads will depend on the compute kernel configuration.
#### unary_ne_tile

void ckernel::unary_ne_tile_init()  

Please refer to documentation for any_init.

void ckernel::unary_ne_tile(uint32_t idst, uint32_t param0)  

Performs element-wise computation of: result = 1 if x!=value , where x is each
element of a tile in DST register at index tile_index. The value is provided
as const param0 The DST register buffer must be in acquired state via
_acquire_dst_ call. This call is blocking and is only available on the compute
engine.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
idst  | The index of the tile in DST register buffer to perform the computation on  | uint32_t  | Must be less than the size of the DST register buffer  | True   
param0  | The value to be compared with the input tensor  | uint32_t  |  | True

#### sub_tiles_bcast

void ckernel::sub_bcast_cols_init_short(uint32_t icb0, uint32_t icb1)  

Performs a first-call or switch-from-another-op tile hw reconfiguration step
needed for sub_bcast_cols to be executed correctly.

template<BroadcastType tBcastDim>  
void ckernel::sub_tiles_bcast(uint32_t icb0, uint32_t icb1, uint32_t itile0,
uint32_t itile1, uint32_t idst)  

Please refer to documentation for _add_tiles_bcast_.
#### gelu_tile

template<bool fast_and_approx = true>  
void ckernel::gelu_tile_init()  

Please refer to documentation for any_init.

template<bool fast_and_approx = true>  
void ckernel::gelu_tile(uint32_t idst)  

Performs element-wise computation of gelu on each element of a tile in DST
register at index tile_index. The DST register buffer must be in acquired
state via _acquire_dst_ call. This call is blocking and is only available on
the compute engine.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
tile_index  | The index of the tile in DST register buffer to perform the computation on  | uint32_t  | Must be less than the size of the DST register buffer  | True   
fast_and_approx  | Computation to be done faster and approximate  | bool  |  | False

#### matmul_block

void ckernel::mm_block_init(uint32_t in0_cb_id, uint32_t in1_cb_id, uint32_t
out_cb_id, const uint32_t transpose = 0, uint32_t ct_dim = 1, uint32_t rt_dim
= 1, uint32_t kt_dim = 1)  

Initialization for matmul_block operation. Must be called before matmul_block.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
in0_cb_id  | The identifier of the first input circular buffer (CB)  | uint32_t  | 0 to 31  | False   
in1_cb_id  | The identifier of the second input circular buffer (CB)  | uint32_t  | 0 to 31  | False   
out_cb_id  | The identifier of the output circular buffer (CB)  | uint32_t  | 0 to 31  | False   
ct_dim  | The number of columns of the output matrix in tiles  | uint32_t  | 1 to 8 in half-sync mode, 1 to 16 in full-sync mode  | False   
rt_dim  | The number of rows of the output matrix in tiles  | uint32_t  | 1 to 8 in half-sync mode, 1 to 16 in full-sync mode  | False   
kt_dim  | The inner dim of the input matrices in tiles  | uint32_t  | 1 to 2^32-1  | False   
  
void ckernel::mm_block_init_short(uint32_t in0_cb_id, uint32_t in1_cb_id,
const uint32_t transpose = 0, uint32_t ct_dim = 1, uint32_t rt_dim = 1,
uint32_t kt_dim = 1)  

A short version of matmul_block initialization. Configure the unpacker and
math engine to matmul mode.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
in0_cb_id  | The identifier of the first input circular buffer (CB)  | uint32_t  | 0 to 31  | False   
in1_cb_id  | The identifier of the second input circular buffer (CB)  | uint32_t  | 0 to 31  | False   
transpose  | The transpose flag for performing transpose operation on B  | uint32_t  | Any positive value will indicate tranpose is set  | False   
ct_dim  | The coloumn dimension for the output block.  | uint32_t  | Must be equal to block B column dimension  | False   
rt_dim  | The row dimension for the output block.  | uint32_t  | Must be equal to block A row dimension  | False   
kt_dim  | The inner dimension.  | uint32_t  | Must be equal to block A column dimension  | False   
  
void ckernel::mm_block_init_short_with_dt(uint32_t in0_cb_id, uint32_t
in1_cb_id, uint32_t old_in1_cb_id, const uint32_t transpose = 0, uint32_t
ct_dim = 1, uint32_t rt_dim = 1, uint32_t kt_dim = 1)  

A short version of matmul_block initialization. It is used to reconfigure srcA
of the compute engine back to matmul mode.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
in0_cb_id  | The identifier of the first input circular buffer (CB)  | uint32_t  | 0 to 31  | False   
in1_cb_id  | The identifier of the second input circular buffer (CB)  | uint32_t  | 0 to 31  | False   
old_in1_cb_id  | The identifier of the old in1_cb_id circular buffer (CB)  | uint32_t  | 0 to 31  | False   
ct_dim  | The coloumn dimension for the output block.  | uint32_t  | Must be equal to block B column dimension  | False   
rt_dim  | The row dimension for the output block.  | uint32_t  | Must be equal to block A row dimension  | False   
kt_dim  | The inner dimension.  | uint32_t  | Must be equal to block A column dimension  | False   
  
void ckernel::matmul_block(uint32_t in0_cb_id, uint32_t in1_cb_id, uint32_t
in0_tile_index, uint32_t in1_tile_index, uint32_t idst, const uint32_t
transpose, uint32_t ct_dim, uint32_t rt_dim, uint32_t kt_dim)  

Performs block-sized matrix multiplication _C=A*B_ between the blocks in two
different input CBs and writes the result to DST. The DST register buffer must
be in acquired state via _acquire_dst_ call. This call is blocking and is only
available on the compute engine.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
in0_cb_id  | The identifier of the first input circular buffer (CB)  | uint32_t  | 0 to 31  | True   
in1_cb_id  | The identifier of the second input circular buffer (CB)  | uint32_t  | 0 to 31  | True   
in0_tile_index  | The index of the tile in block A from the first input CB  | uint32_t  | Must be less than the size of the CB  | True   
in1_tile_index  | The index of the tile in block B from the second input CB  | uint32_t  | Must be less than the size of the CB  | True   
idst  | The index of the tile in DST REG to which the result C will be written.  | uint32_t  | Must be less than the acquired size of DST REG  | True   
transpose  | The transpose flag for performing transpose operation on tiles in B.  | bool  | Must be true or false  | True   
ct_dim  | The coloumn dimension for the output block.  | uint32_t  | Must be equal to block B column dimension  | True   
rt_dim  | The row dimension for the output block.  | uint32_t  | Must be equal to block A row dimension  | True   
kt_dim  | The inner dimension.  | uint32_t  | Must be equal to block A column dimension  | True

#### lez_tile

void ckernel::lez_tile_init()  

Please refer to documentation for any_init.

void ckernel::lez_tile(uint32_t idst)  

Will store in the output of the compute core True if each element is less than
or equal to zero. The DST register buffer must be in acquired state via
_acquire_dst_ call. This call is blocking and is only available on the compute
engine.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
idst  | The index of the tile in DST register buffer to perform the computation on  | uint32_t  | Must be less than the size of the DST register buffer  | True

#### reg_api

void ckernel::tile_regs_acquire()  

Acquire an exclusive lock on the DST register for the MATH thread. This
register is an array of 16 tiles of 32x32 elements each. This is a blocking
function, i.e. this function will wait until the lock is acquired.

void ckernel::tile_regs_wait()  

Acquire an exclusive lock on the DST register for the PACK thread. It waits
for the MATH thread to commit the DST register. This is a blocking function,
i.e. this function will wait until the lock is acquired.

void ckernel::tile_regs_commit()  

Release lock on DST register by MATH thread. The lock had to be previously
acquired with tile_regs_acquire.

void ckernel::tile_regs_release()  

Release lock on DST register by PACK thread. The lock had to be previously
acquired with tile_regs_wait.
#### tanh_tile

void ckernel::tanh_tile_init()  

Please refer to documentation for any_init.

void ckernel::tanh_tile(uint32_t idst)  

Performs element-wise computation of tanh on each element of a tile in DST
register at index tile_index. The DST register buffer must be in acquired
state via _acquire_dst_ call. This call is blocking and is only available on
the compute engine.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
idst  | The index of the tile in DST register buffer to perform the computation on  | uint32_t  | Must be less than the size of the DST register buffer  | True

#### sin_tile

void ckernel::sin_tile_init()  

Please refer to documentation for any_init.

void ckernel::sin_tile(uint32_t idst)  

Performs element-wise computation of the trigonometric sine operation on each
element of a tile in DST register at index tile_index. The DST register buffer
must be in acquired state via _acquire_dst_ call. This call is blocking and is
only available on the compute engine.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
tile_index  | The index of the tile in DST register buffer to perform the computation on  | uint32_t  | Must be less than the size of the DST register buffer  | True

#### log_tile

void ckernel::log_tile_init()  

Please refer to documentation for any_init.

void ckernel::log_tile(uint32_t idst)  

Performs element-wise computation of logarithm on each element of a tile in
DST register at index tile_index. The DST register buffer must be in acquired
state via _acquire_dst_ call. This call is blocking and is only available on
the compute engine.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
idst  | The index of the tile in DST register buffer to perform the computation on  | uint32_t  | Must be less than the size of the DST register buffer  | True

#### gez_tile

void ckernel::gez_tile_init()  

Please refer to documentation for any_init.

void ckernel::gez_tile(uint32_t idst)  

Will store in the output of the compute core True if each element is greater
than or equal to zero. The DST register buffer must be in acquired state via
_acquire_dst_ call. This call is blocking and is only available on the compute
engine.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
idst  | The index of the tile in DST register buffer to perform the computation on  | uint32_t  | Must be less than the size of the DST register buffer  | True

#### cb_reserve_back

void ckernel::cb_reserve_back(uint32_t cbid, uint32_t ntiles)  

A blocking call that waits for the specified number of tiles to be free in the
specified circular buffer. This call is used by the producer to wait for the
consumer to consume (ie. free up) the specified number of tiles.

CB total size must be an even multiple of the argument passed to this call.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
cb_id  | The index of the cirular buffer (CB)  | uint32_t  | 0 to 31  | True   
ntiles  | The number of free tiles to wait for  | uint32_t  | It must be less or equal than the size of the CB (the total number of tiles that fit into the CB)  | True

#### sqrt_tile

void ckernel::sqrt_tile_init()  

Please refer to documentation for any_init.

void ckernel::sqrt_tile(uint32_t idst)  

Performs element-wise computation of the square root on each element of a tile
in DST register at index tile_index. The DST register buffer must be in
acquired state via _acquire_dst_ call. This call is blocking and is only
available on the compute engine.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
tile_index  | The index of the tile in DST register buffer to perform the computation on  | uint32_t  | Must be less than the size of the DST register buffer  | True

#### add_tiles

void ckernel::add_tiles_init_nof()  

Please refer to documentation for any_init. nof means low fidelity with
resepect to accuracy this is set during createprogram

void ckernel::add_tiles_init(uint32_t icb0, uint32_t icb1, bool acc_to_dest =
false)  

Short init function

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
icb0  | The identifier of the circular buffer (CB) containing A  | uint32_t  | 0 to 31  | True   
icb1  | The identifier of the circular buffer (CB) containing B  | uint32_t  | 0 to 31  | True   
acc_to_dest  | If true, operation = A + B + dst_tile_idx of add_tiles  | bool  | 0,1  | False   
  
void ckernel::add_tiles(uint32_t icb0, uint32_t icb1, uint32_t itile0,
uint32_t itile1, uint32_t idst)  

Performs element-wise addition C=A+B of tiles in two CBs at given indices and
writes the result to the DST register at index dst_tile_index. The DST
register buffer must be in acquired state via _acquire_dst_ call. This call is
blocking and is only available on the compute engine.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
in0_cb_id  | The identifier of the circular buffer (CB) containing A  | uint32_t  | 0 to 31  | True   
in1_cb_id  | The identifier of the circular buffer (CB) containing B  | uint32_t  | 0 to 31  | True   
in0_tile_index  | The index of tile A within the first CB  | uint32_t  | Must be less than the size of the CB  | True   
in1_tile_index  | The index of tile B within the second CB  | uint32_t  | Must be less than the size of the CB  | True   
dst_tile_index  | The index of the tile in DST REG for the result C  | uint32_t  | Must be less than the acquired size of DST REG  | True

#### recip_tile

void ckernel::recip_tile_init()  

Please refer to documentation for any_init.

void ckernel::recip_tile(uint32_t idst)  

Performs element-wise computation of the reciprocal on each element of a tile
in DST register at index tile_index. The DST register buffer must be in
acquired state via _acquire_dst_ call. This call is blocking and is only
available on the compute engine. Only works for Float32, Float16_b, Bfp8_b
data formats for full accuracy.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
idst  | The index of the tile in DST register buffer to perform the computation on  | uint32_t  | Must be less than the size of the DST register buffer  | True

#### signbit_tile

void ckernel::signbit_tile_init()  

Please refer to documentation for any_init.

void ckernel::signbit_tile(uint32_t idst)  

Sets the sign bit of each element of a tile in DST register at index
tile_index. The DST register buffer must be in acquired state via
_acquire_dst_ call. This call is blocking and is only available on the compute
engine.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
idst  | The index of the tile in DST register buffer to modify the sign bit of  | uint32_t  | Must be less than the size of the DST register buffer  | True

#### sigmoid_tile

void ckernel::sigmoid_tile_init()  

Please refer to documentation for any_init.

void ckernel::sigmoid_tile(uint32_t idst)  

Performs element-wise computation of sigmoid on each element of a tile in DST
register at index tile_index. The DST register buffer must be in acquired
state via _acquire_dst_ call. This call is blocking and is only available on
the compute engine.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
idst  | The index of the tile in DST register buffer to perform the computation on  | uint32_t  | Must be less than the size of the DST register buffer  | True

#### tilize

void ckernel::tilize_init(uint32_t icb, uint32_t block, uint32_t ocb)  

Initialize the tilize operation. To be called once at beginning of a kernel.

void ckernel::tilize_init_short(uint32_t icb, uint32_t block, uint32_t ocb)  

Re-initialize for the tilize operation. This can be called after a full init.

void ckernel::tilize_init_short_with_dt(uint32_t old_icb, uint32_t new_icb,
uint32_t block, uint32_t ocb)  

Re-initialize for the tilize operation. This also reconfigure the unpacker
with CB data type.

void ckernel::tilize_block(uint32_t icb, uint32_t block, uint32_t ocb)  

Perform tilize operation on a block. This simply loops over the provided
blocks.

void ckernel::tilize_uninit(uint32_t icb, uint32_t ocb)  

Uninitialize tilize operation before re-initializing for another operation.

void ckernel::tilize_uninit_with_dt(uint32_t old_icb, uint32_t new_icb,
uint32_t ocb)  

Uninitialize the tilize operation along with re-configuring unpacker with the
CB data types.
#### erf_tile

template<bool fast_and_approx = true>  
void ckernel::erf_tile_init()  

Please refer to documentation for any_init.

template<bool fast_and_approx = true>  
void ckernel::erf_tile(uint32_t idst)  

Performs element-wise computation of error function on each element of a tile
in DST register at index tile_index. The DST register buffer must be in
acquired state via _acquire_dst_ call. This call is blocking and is only
available on the compute engine.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
tile_index  | The index of the tile in DST register buffer to perform the computation on  | uint32_t  | Must be less than the size of the DST register buffer  | True

#### rsub_tile

void ckernel::rsub_tile_init()  

Please refer to documentation for any_init.

void ckernel::rsub_tile(uint32_t idst, uint32_t param0)  

Performs element-wise computation of rsub ( rsub(x,y) = y -x) on each element
of a tile and y is a constant param in DST register at index tile_index. The
DST register buffer must be in acquired state via _acquire_dst_ call. This
call is blocking and is only available on the compute engine.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
idst  | The index of the tile in DST register buffer to perform the computation on  | uint32_t  | Must be less than the size of the DST register buffer  | True   
param0  | Constant value that is being subtracted from  | uint32_t  |  | True

#### cb_wait_front

void ckernel::cb_wait_front(uint32_t cbid, uint32_t ntiles)  

A blocking call that waits for the specified number of tiles to be available
in the specified circular buffer (CB). This call is used by the consumer of
the CB to wait for the producer to fill the CB with at least the specfied
number of tiles. Important note: in case multiple calls of cb_wait_front(n)
are issued without a paired
[cb_pop_front()](cb_pop_front.html#namespaceckernel_1a09e8d82ba4b886f8e90eec038735d759)
call, n is expected to be incremented by the user to be equal to a cumulative
total of tiles. Example: 4 calls of cb_wait_front(8) followed by a
cb_pop_front(32) would produce incorrect behavior. Instead 4 calls of
cb_wait_front() waiting on 8, 16, 24, 32 tiles should be issued.

Important note: number of tiles used in all cb_* calls must evenly divide the
cb size and must be the same number in all cb_wait_front calls in the same
kernel. Example 1: cb_wait_front(32), cb_wait_front(40), cb_pop_front(32+8)
tiles on a CB of size 64 would produce incorrect behavior. Example 2:
cb_wait_front(3) on a cb of size 32 would also produce incorrect behavior.
These limitations are due to performance optimizations in the CB
implementation.

Important note: CB total size must be an even multiple of the argument passed
to this call.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
cb_id  | The index of the cirular buffer (CB)  | uint32_t  | 0 to 31  | True   
ntiles  | The number of tiles to wait for  | uint32_t  | It must be less or equal than the size of the CB (the total number of tiles that fit into the CB)  | True

#### i0_tile

void ckernel::i0_tile_init()  

Please refer to documentation for any_init.

void ckernel::i0_tile(uint32_t idst)  

Performs element-wise computation of the zeroth order modified Bessel function
of the first kind on each element of a tile in DST register at index
tile_index. The DST register buffer must be in acquired state via
_acquire_dst_ call. This call is blocking and is only available on the compute
engine.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
tile_index  | The index of the tile in DST register buffer to perform the computation on  | uint32_t  | Must be less than the size of the DST register buffer  | True

#### cb_push_back

void ckernel::cb_push_back(uint32_t cbid, uint32_t ntiles)  

Pushes a given number of tiles in the back of the specified CB’s queue.
Decreases the available space in the circular buffer by this number of tiles.
This call is used by the producer to make the tiles visible to the consumer of
the CB.

We use the convention that the producer pushes tiles into the “back” of the CB
queue and the consumer consumes tiles from the “front” of the CB queue.

Note that the act of writing the tile data into the CB does not make the tiles
visible to the consumer. Writing of the tiles and pushing is separated to
allow the producer to: 1) write the tile data to the CB via multiple writes of
sub-tiles 2) modify tiles (or sub-tiles) by random access of the valid section
of the CB

Important note: This operation updates the write pointer of the CB, the CB
pointer can only be updated from one thread at a time. Example: if compute
kernel has cb_push_back(output_id, 1) and reader kernel also has
cb_push_back(output_id, 1), these calls will produce non-deterministic
behavior because cb pointers are not synchronized across threads. Per circular
buffer index, only have one thread push tiles to update the write pointer

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
cb_id  | The index of the cirular buffer (CB)  | uint32_t  | 0 to 31  | True   
ntiles  | The number of tiles to be pushed  | uint32_t  | It must be less or equal than the size of the CB (the total number of tiles that fit into the CB)  | True

#### cb_pop_front

void ckernel::cb_pop_front(uint32_t cbid, uint32_t ntiles)  

Pops a specified number of tiles from the front of the specified CB. This also
frees this number of tiles in the circular buffer. This call is used by the
consumer to free up the space in the CB.

We use the convention that the producer pushes tiles into the “back” of the CB
queue and the consumer consumes tiles from the “front” of the CB queue.

Note that the act of reading of the tile data from the CB does not free up the
space in the CB. Waiting on available tiles and popping them is separated in
order to allow the consumer to: 1) read the tile data from the CB via multiple
reads of sub-tiles 2) access the tiles (or their sub-tiles) that are visible
to the consumer by random access of the valid section of the CB

Important note: This operation updates the read pointer of the CB, the CB
pointer can only be updated from one thread at a time. Example: if compute
kernel has cb_pop_front(input_id, 1) and writer kernel also has
cb_pop_front(input_id, 1), these calls will produce non-deterministic behavior
because cb pointers are not synchronized across threads. Per circular buffer
index, only have one thread pop tiles to update the read pointer

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
cb_id  | The index of the cirular buffer (CB)  | uint32_t  | 0 to 31  | True   
ntiles  | The number of tiles to be popped  | uint32_t  | It must be less or equal than the size of the CB (the total number of tiles that fit into the CB)  | True

#### erfinv_tile

void ckernel::erfinv_tile_init()  

Please refer to documentation for any_init.

void ckernel::erfinv_tile(uint32_t idst)  

Performs element-wise computation of the inverse of the error function on each
element of a tile in DST register at index tile_index. The DST register buffer
must be in acquired state via _acquire_dst_ call. This call is blocking and is
only available on the compute engine.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
tile_index  | The index of the tile in DST register buffer to perform the computation on  | uint32_t  | Must be less than the size of the DST register buffer  | True

#### reduce_tile

template<PoolType reduce_type = REDUCE_OP, ReduceDim reduce_dim = REDUCE_DIM>  
void ckernel::reduce_tile(uint32_t icb0, uint32_t icb1, uint32_t itile0,
uint32_t itile1, uint32_t idst)  

Performs a reduction operation _B = reduce(A)_ using reduce_func for dimension
reduction on a tile in the CB at a given index and writes the result to the
DST register at index _dst_tile_index_. Reduction can be either of type
_Reduce::R_ , _Reduce::C_ or _Reduce::RC_ , identifying the dimension(s) to be
reduced in size to 1. The DST register buffer must be in acquired state via
_acquire_dst_ call.

The templates takes reduce_type which can be ReduceFunc::Sum, ReduceFunc::Max
and reduce_dim which can be Reduce::R, Reduce::C, Reduce::RC. They can also be
specified by defines REDUCE_OP and REDUCE_DIM.

This call is blocking and is only available on the compute engine.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
icb0  | The identifier of the circular buffer (CB) containing A  | uint32_t  | 0 to 31  | True   
icb1  | CB for Scaling factor applied to each element of the result.  | uint32_t  | 0 to 31  | True   
itile0  | The index of the tile within the first CB  | uint32_t  | Must be less than the size of the CB  | True   
itile1  | The index of the tile within the scaling factor CB.  | uint32_t  | Must be less than the size of the CB  | True   
idst  | The index of the tile in DST REG for the result  | uint32_t  | Must be less than the acquired size of DST REG  | True

#### isnan_tile

void ckernel::isnan_tile(uint32_t idst)  

Will store in the output of the compute core True if the input tile is nan.
The DST register buffer must be in acquired state via _acquire_dst_ call. This
call is blocking and is only available on the compute engine.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
tile_index  | The index of the tile in DST register buffer to perform the computation on  | uint32_t  | Must be less than the size of the DST register buffer  | True

#### rsqrt_tile

template<bool fast_and_approx = true>  
void ckernel::rsqrt_tile_init()  

Please refer to documentation for any_init.

template<bool fast_and_approx = true>  
void ckernel::rsqrt_tile(uint32_t idst)  

Performs element-wise computation of reciprocal sqrt on each element of a tile
in DST register at index tile_index. The DST register buffer must be in
acquired state via _acquire_dst_ call. This call is blocking and is only
available on the compute engine.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
idst  | The index of the tile in DST register buffer to perform the computation on  | uint32_t  | Must be less than the size of the DST register buffer  | True   
fast_and_approx  | Computation to be done faster and approximate  | bool  |  | False

#### asin_tile

void ckernel::asin_tile_init()  

Please refer to documentation for any_init.

void ckernel::asin_tile(uint32_t idst)  

Performs element-wise computation of arcsine on each element of a tile in DST
register at index tile_index. The DST register buffer must be in acquired
state via _acquire_dst_ call. This call is blocking and is only available on
the compute engine.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
idst  | The index of the tile in DST register buffer to perform the computation on  | uint32_t  | Must be less than the size of the DST register buffer  | True

#### square_tile

void ckernel::square_tile_init()  

Please refer to documentation for any_init.

void ckernel::square_tile(uint32_t idst)  

Performs element-wise computation of square value on each element of a tile in
DST register at index tile_index. The DST register buffer must be in acquired
state via _acquire_dst_ call. This call is blocking and is only available on
the compute engine.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
idst  | The index of the tile in DST register buffer to perform the computation on  | uint32_t  | Must be less than the size of the DST register buffer  | True

#### sub_tiles

void ckernel::sub_tiles_init_nof()  

Please refer to documentation for any_init. nof means low fidelity with
respect to accuracy this is set during createprogram

void ckernel::sub_tiles_init(uint32_t icb0, uint32_t icb1, bool acc_to_dest =
false)  

Short init function

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
icb0  | The identifier of the circular buffer (CB) containing A  | uint32_t  | 0 to 31  | True   
icb1  | The identifier of the circular buffer (CB) containing B  | uint32_t  | 0 to 31  | True   
acc_to_dest  | If true, operation = A - B + dst_tile_idx of sub_tiles  | bool  | 0,1  | False   
  
void ckernel::sub_tiles(uint32_t icb0, uint32_t icb1, uint32_t itile0,
uint32_t itile1, uint32_t idst)  

Performs element-wise subtraction C=A-B of tiles in two CBs at given indices
and writes the result to the DST register at index dst_tile_index. The DST
register buffer must be in acquired state via _acquire_dst_ call. This call is
blocking and is only available on the compute engine.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
in0_cb_id  | The identifier of the circular buffer (CB) containing A  | uint32_t  | 0 to 31  | True   
in1_cb_id  | The identifier of the circular buffer (CB) containing B  | uint32_t  | 0 to 31  | True   
in0_tile_index  | The index of tile A within the first CB  | uint32_t  | Must be less than the size of the CB  | True   
in1_tile_index  | The index of tile B within the second CB  | uint32_t  | Must be less than the size of the CB  | True   
dst_tile_index  | The index of the tile in DST REG for the result C  | uint32_t  | Must be less than the acquired size of DST REG  | True

#### binary_init_funcs

void ckernel::binary_op_init_common(uint32_t icb0, uint32_t icb1, uint32_t
ocb)  

Init function for all binary ops Followed by the specific init required with
an opcode (binrary_op_specific_init)

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
icb0  | The identifier of the circular buffer (CB) containing A  | uint32_t  | 0 to 31  | True   
icb1  | The identifier of the circular buffer (CB) containing B  | uint32_t  | 0 to 31  | True   
ocb  | The identifier of the circular buffer (CB) containing output  | uint32_t  | 0 to 31, defaults to CB 16  | True   
  
template<bool full_init = false, EltwiseBinaryType eltwise_binary_op_type =
ELWADD>  
void ckernel::binary_op_specific_init(uint32_t icb0, uint32_t icb1)  

Init function with a specified op template parameters: full_init: if true, the
full init is performed (unpack+math), otherwise a nof init is performed (only
math) eltwise_binary_op_type: the binary operation type
#### exp2_tile

void ckernel::exp2_tile_init()  

Please refer to documentation for any_init.

void ckernel::exp2_tile(uint32_t idst)  

Performs element-wise computation of 2^x value where x is each element of a
tile in DST register at index tile_index. The DST register buffer must be in
acquired state via _acquire_dst_ call. This call is blocking and is only
available on the compute engine.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
idst  | The index of the tile in DST register buffer to perform the computation on  | uint32_t  | Must be less than the size of the DST register buffer  | True

#### expm1_tile

void ckernel::expm1_tile_init()  

Please refer to documentation for any_init.

void ckernel::expm1_tile(uint32_t idst)  

Performs element-wise computation of exp(x) - 1, v where x is each element of
a tile in DST register at index tile_index. The DST register buffer must be in
acquired state via _acquire_dst_ call. This call is blocking and is only
available on the compute engine.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
idst  | The index of the tile in DST register buffer to perform the computation on  | uint32_t  | Must be less than the size of the DST register buffer  | True

#### acquire_dst

void ckernel::acquire_dst()  

_Deprecated:_

This function is deprecated, please use
`[tile_regs_acquire()](reg_api.html#namespaceckernel_1a34467f46da4221ff3a2820ff1baec122)`
instead. See <https://github.com/tenstorrent/tt-metal/issues/5868#issuecomment-2101726935>

Acquires an exclusive lock on the internal DST register for the current Tensix
core.

This register is an array of 16 tiles of 32x32 elements each. This is a
blocking function, i.e. this function will wait until the lock is acquired.

This is only available on the compute engine.

Return value: None

How the destination register will be shared and synchronized between TRISC
threads will depend on the compute kernel configuration.
#### exp_tile

template<bool fast_and_approx = false>  
void ckernel::exp_tile_init()  

Please refer to documentation for any_init.

template<bool fast_and_approx = false>  
void ckernel::exp_tile(uint32_t idst)  

Performs element-wise computation of exponential on each element of a tile in
DST register at index tile_index. The DST register buffer must be in acquired
state via _acquire_dst_ call. This call is blocking and is only available on
the compute engine.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
tile_index  | The index of the tile in DST register buffer to perform the computation on  | uint32_t  | Must be less than the size of the DST register buffer  | True   
fast_and_approx  | Computation to be done faster and approximate  | bool  |  | False

#### any_init

Most compute API calls have an *_init paired API call (for example
exp_tile_init and exp_tile). Invoking this *_init API configures the compute
unit for execution of the subsequent paired call.
#### abs_tile

void ckernel::abs_tile_init()  

Please refer to documentation for any_init.

void ckernel::abs_tile(uint32_t idst)  

Performs element-wise computation of absolute value on each element of a tile
in DST register at index tile_index. The DST register buffer must be in
acquired state via _acquire_dst_ call. This call is blocking and is only
available on the compute engine.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
idst  | The index of the tile in DST register buffer to perform the computation on  | uint32_t  | Must be less than the size of the DST register buffer  | True 