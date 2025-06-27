### Circular Buffers
#### cb_pages_available_at_front

bool cb_pages_available_at_front(int32_t operand, int32_t num_pages)  

    

A non-blocking call that tells the caller if the specified number of pages are
available in the specified circular buffer (CB). This call is used by the
consumer of the CB to see if the prodcuers has fill the CB with at least the
specified number of tiles. Important note: in case multiple calls of
cb_wait_front(n) are issued without a paired
[cb_pop_front()](cb_pop_front.html#dataflow__api_8h_1aa3daf8e5e7299140cf2607be1a8656b0)
call, n is expected to be incremented by the user to be equal to a cumulative
total of tiles. Example: 4 calls of cb_wait_front(8) followed by a
cb_pop_front(32) would produce incorrect behavior. Instead 4 calls of
[cb_wait_front()](cb_wait_front.html#dataflow__api_8h_1af6d8057bd05a650c3501c5208f7d9f8a)
waiting on 8, 16, 24, 32 tiles should be issued.

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
cb_id  | The index of the circular buffer (CB)  | uint32_t  | 0 to 31  | True   
num_tiles  | The number of tiles to check for  | uint32_t  | It must be less or equal than the size of the CB (the total number of tiles that fit into the CB)  | 



#### cb_reserve_back

void cb_reserve_back(int32_t operand, int32_t num_pages)  

    

A blocking call that waits for the specified number of tiles to be free in the
specified circular buffer. This call is used by the producer to wait for the
consumer to consume (ie. free up) the specified number of tiles.

CB total size must be an even multiple of the argument passed to this call.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
cb_id  | The index of the circular buffer (CB)  | uint32_t  | 0 to 31  | True   
num_tiles  | The number of free tiles to wait for  | uint32_t  | It must be less or equal than the size of the CB (the total number of tiles that fit into the CB)  | True 



#### cb_pages_reservable_at_back

bool cb_pages_reservable_at_back(int32_t operand, int32_t num_pages)  

    

A non-blocking call that checks if the specified number of pages are available
for reservation at the back of the circular buffer. This call is used by the
producer to see if the consumer has freed up the desired space (in pages).

CB total size must be an even multiple of the argument passed to this call.

Return value: true if the specified number of pages are available

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
cb_id  | The index of the circular buffer (CB)  | uint32_t  | 0 to 31  | True   
num_tiles  | The number of free tiles to wait for  | uint32_t  | It must be less or equal than the size of the CB (the total number of tiles that fit into the CB)  | True 



#### cb_wait_front

void cb_wait_front(int32_t operand, int32_t num_pages)  

    

A blocking call that waits for the specified number of tiles to be available
in the specified circular buffer (CB). This call is used by the consumer of
the CB to wait for the producer to fill the CB with at least the specified
number of tiles. Important note: in case multiple calls of cb_wait_front(n)
are issued without a paired
[cb_pop_front()](cb_pop_front.html#dataflow__api_8h_1aa3daf8e5e7299140cf2607be1a8656b0)
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
cb_id  | The index of the circular buffer (CB)  | uint32_t  | 0 to 31  | True   
num_tiles  | The number of tiles to wait for  | uint32_t  | It must be less or equal than the size of the CB (the total number of tiles that fit into the CB)  | 



#### cb_push_back

void cb_push_back(const int32_t operand, const int32_t num_pages)  

    

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

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
cb_id  | The index of the circular buffer (CB)  | uint32_t  | 0 to 31  | True   
num_tiles  | The number of tiles to be pushed  | uint32_t  | It must be less or equal than the size of the CB (the total number of tiles that fit into the CB)  | True 



#### cb_pop_front

void cb_pop_front(int32_t operand, int32_t num_pages)  

    

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

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
cb_id  | The index of the circular buffer (CB)  | uint32_t  | 0 to 31  | True   
num_tiles  | The number of tiles to be popped  | uint32_t  | It must be less or equal than the size of the CB (the total number of tiles that fit into the CB)  | True 



#### Circular Buffer APIs

Circular buffers are used for communication between threads of the Tensix
core. They act as limited capacity double-ended queues with producers pushing
tiles to the back of the queue and consumers popping tiles off the front of
the queue.

  * [cb_pages_available_at_front](cb_pages_available_at_front.html)
  * [cb_wait_front](cb_wait_front.html)
  * [cb_pages_reservable_at_back](cb_pages_reservable_at_back.html)
  * [cb_reserve_back](cb_reserve_back.html)
  * [cb_push_back](cb_push_back.html)
  * [cb_pop_front](cb_pop_front.html)



### Compute Operations
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



#### copy_tile

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



#### erfc_tile

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
instead. See <https://github.com/tenstorrent/tt-
metal/issues/5868#issuecomment-2101726935>

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



### Data Movement
#### noc_semaphore_inc

void noc_semaphore_inc(uint64_t addr, uint32_t incr, uint8_t noc_id =
noc_index)  

    

The Tensix core executing this function call initiates an atomic increment
(with 32-bit wrap) of a remote Tensix core L1 memory address. This L1 memory
address is used as a semaphore of size 4 Bytes, as a synchronization
mechanism.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
addr  | Encoding of the destination location (x,y)+address  | uint64_t  | DOX-TODO(insert a reference to what constitutes valid coords)  | True   
incr  | The value to increment by  | uint32_t  | Any uint32_t value  | True 



#### Ordering (NOC, CMD_BUF, VC)

NoC requests/responses are usually asynchronous, but they can have an implicit
ordering, or you could enforce an explicit ordering. In this section, we will
go over command buffers (CMD_BUF), virtual channels (VC), and allocation of
virtual channels.

There are two NoCs (NoC-0 and NoC-1) that are completely phyiscally replicated
and separated. The only communication between these NoCs is through software
or L1 memory. For each NoC, we have 4 command buffers: RD_CMD_BUF, WR_CMD_BUF,
WR_REG_CMD_BUF, AT_CMD_BUF. We usually use the WR_CMD_BUF for all writes,
except for the atomic ones where we use AT_CMD_BUF, e.g. noc_semaphore_inc
uses AT_CMD_BUF.

For each NoC, we have 6 VC (numbered 0-5). Each VC is usually used for a
different purpose. For example, all unicast writes go on NOC_UNICAST_WRITE_VC,
which is VC 1, and all multicast writes go on NOC_MULTICAST_WRITE_VC, which is
VC 4.

We can allocate VC either statically or dynamically. We can allocate VC
statically using NOC_CMD_STATIC_VC, which is usually the case for noc writes.
For noc reads, the read requests can use a statically allocated VC, as for
read responses, we always use dynamically allocated VC. So there’s really no
way to control ordering for data reads.

As for ordering of the NoC writes:

  * If writes are on different NoCs, there is no ordering guarantees.

  * If writes are on the same NoC but different VCs, there’s also no ordering guarantees. You might as well use different CMD_BUFs to avoid serialization.

  * If writes are on the same NoC and same VC, they will be ordered based on program order, regardless whether you use the same CMD_BUF or different ones.



#### noc_async_write_multicast

template<uint32_t max_page_size = NOC_MAX_BURST_SIZE + 1>  
inline void noc_async_write_multicast(std::uint32_t src_local_l1_addr,
std::uint64_t dst_noc_addr_multicast, std::uint32_t size, std::uint32_t
num_dests, bool linked = false, bool multicast_path_reserve = true, uint8_t
noc = noc_index)  

    

Initiates an asynchronous write from a source address in L1 memory on the
Tensix core executing this function call to a rectangular destination grid.
The destinations are specified using a uint64_t encoding referencing an on-
chip grid of nodes located at NOC coordinate range
(x_start,y_start,x_end,y_end) and a local address created using
_get_noc_multicast_addr_ function. Also, _see noc_async_write_barrier_.

The destination nodes can only be a set of Tensix cores + L1 memory address.
The destination nodes must form a rectangular grid. The destination L1 memory
address must be the same on all destination nodes.

With this API, the multicast sender cannot be part of the multicast
destinations. If the multicast sender has to be in the multicast destinations
(i.e. must perform a local L1 write), the other API variant
_noc_async_write_multicast_loopback_src_ can be used.

Note: The number of destinations needs to be non-zero. Besides that, there is
no restriction on the number of destinations, i.e. the multicast destinations
can span the full chip. However, as mentioned previously, the multicast source
cannot be part of the destinations. So, the maximum number of destinations is
number of cores - 1.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
src_local_l1_addr  | Source address in local L1 memory  | uint32_t  | 0..1MB  | True   
dst_noc_addr_multicast  | Encoding of the destinations nodes (x_start,y_start,x_end,y_end)+address  | uint64_t  | DOX-TODO(insert a reference to what constitutes valid coords)  | True   
size  | Size of data transfer in bytes  | uint32_t  | 0..1MB  | True   
num_dests  | Number of destinations that the multicast source is targetting  | uint32_t  | 0..(number of cores -1)  | True 



#### noc_semaphore_set

void noc_semaphore_set(volatile uint32_t *sem_addr, uint32_t val)  

    

Sets the value of a local L1 memory address on the Tensix core executing this
function to a specific value. This L1 memory address is used as a semaphore of
size 4 Bytes, as a synchronization mechanism. Also, see _noc_semaphore_wait_.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
sem_addr  | Semaphore address in local L1 memory  | uint32_t  | 0..1MB  | True   
val  | Value to set the semaphore to  | uint32_t  | Any uint32_t value  | True 



#### Data Movement APIs

  * [noc_async_read](noc_async_read.html)
  * [noc_async_write](noc_async_write.html)
  * [noc_async_read_barrier](noc_async_read_barrier.html)
  * [noc_async_write_barrier](noc_async_write_barrier.html)
  * [noc_async_write_multicast](noc_async_write_multicast.html)
  * [noc_semaphore_set_multicast](noc_semaphore_set_multicast.html)
  * [noc_semaphore_set](noc_semaphore_set.html)
  * [noc_semaphore_wait](noc_semaphore_wait.html)
  * [noc_semaphore_inc](noc_semaphore_inc.html)
  * [Ordering (NOC, CMD_BUF, VC)](ordering.html)



#### noc_async_read_barrier

void noc_async_read_barrier(uint8_t noc = noc_index)  

    

Initiates an asynchronous write from a source address in L1 memory on the
Tensix core executing this function call to an L-shaped destination which is
defined by a grid and an exclusion zone. The destinations are specified using
a uint64_t encoding referencing an on-chip grid of nodes located at NOC
coordinate range (x_start,y_start,x_end,y_end) and a local address created
using _get_noc_multicast_addr_ function. Also, _see noc_async_write_barrier_.
Similarly, the exclusion zone is specified using uint32_t encoding referencing
an on-chip core and directions relative to it created using
_get_noc_exclude_region_ function.

The destination nodes can only be a set of Tensix cores + L1 memory address.
The destination nodes must form an L-shaped grid (where dst_noc_addr_multicast
defines a grid and exclude_region define a subgrid to exclude, the inner part
of the L). The destination L1 memory address must be the same on all
destination nodes.

With this API, the multicast sender cannot be part of the multicast
destinations.

Note: The number of destinations needs to be non-zero. Besides that, there is
no restriction on the number of destinations, i.e. the multicast destinations
can span the full chip. However, as mentioned previously, the multicast source
cannot be part of the destinations. So, the maximum number of destinations is
number of cores - 1.

Return value: None

NOTE: only supported on Blackhole

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
src_local_l1_addr  | Source address in local L1 memory  | uint32_t  | 0..1MB  | True   
dst_noc_addr_multicast  | Encoding of the destinations nodes (x_start,y_start,x_end,y_end)+address  | uint64_t  | DOX-TODO(insert a reference to what constitutes valid coords)  | True   
size  | Size of data transfer in bytes  | uint32_t  | 0..1MB  | True   
num_dests  | Number of destinations that the multicast source is targetting  | uint32_t  | 0..(number of cores - 1)  | True   
exclude_region  | Encoding of the excluded region (x_start,y_start,x_direction,y_direction)  | uint32_t  | DOX-TODO(insert a reference to what constitutes valid coords)  | True   
This blocking call waits for all the outstanding enqueued _noc_async_read_
calls issued on the current Tensix core to complete. After returning from this
call the _noc_async_read_ queue will be empty for the current Tensix core.

Return value: None



#### noc_async_read

template<uint32_t max_page_size>  
inline void noc_async_read(std::uint64_t src_noc_addr, std::uint32_t
dst_local_l1_addr, std::uint32_t size, uint8_t noc)  

    

Initiates an asynchronous read from a specified source node located at NOC
coordinates (x,y) at a local address (encoded as a uint64_t using
_get_noc_addr_ function). The destination is in L1 memory on the Tensix core
executing this function call. Also, see _noc_async_read_barrier_.

The source node can be either a DRAM bank, a Tensix core or a PCIe controller.

Return value: None

Argument  | Description  | Data type  | Valid range  | required   
---|---|---|---|---  
src_noc_addr  | Encoding of the source NOC location (x,y)+address  | uint64_t  | DOX-TODO (ref to explain valid coords)  | Yes   
dst_local_l1_addr  | Address in local L1 memory  | uint32_t  | 0..1MB  | Yes   
size  | Size of data transfer in bytes  | uint32_t  | 0..1MB  | Yes 



#### noc_semaphore_set_multicast

inline void noc_semaphore_set_multicast(std::uint32_t src_local_l1_addr,
std::uint64_t dst_noc_addr_multicast, std::uint32_t num_dests, bool linked =
false, bool multicast_path_reserve = true, uint8_t noc = noc_index)  

    

Initiates an asynchronous write from a source address in L1 memory on the
Tensix core executing this function call to a rectangular destination grid.
The destinations are specified using a uint64_t encoding referencing an on-
chip grid of nodes located at NOC coordinate range
(x_start,y_start,x_end,y_end) and a local address created using
_get_noc_multicast_addr_ function. The size of data that is sent is 4 Bytes.
This is usually used to set a semaphore value at the destination nodes, as a
way of a synchronization mechanism. The same as _noc_async_write_multicast_
with preset size of 4 Bytes.

With this API, the multicast sender cannot be part of the multicast
destinations. If the multicast sender has to be in the multicast destinations
(i.e. must perform a local L1 write), the other API variant
_noc_semaphore_set_multicast_loopback_src_ can be used.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
src_local_l1_addr  | Source address in local L1 memory  | uint32_t  | 0..1MB  | True   
dst_noc_addr_multicast  | Encoding of the destinations nodes (x_start,y_start,x_end,y_end)+address  | uint64_t  | DOX-TODO(insert a reference to what constitutes valid coords)  | True   
num_dests  | Number of destinations that the multicast source is targetting  | uint32_t  | 0..(number of cores - 1)  | True 



#### noc_async_write_barrier

void noc_async_write_barrier(uint8_t noc = noc_index)  

    

This blocking call waits for all the outstanding enqueued _noc_async_write_
calls issued on the current Tensix core to complete. After returning from this
call the _noc_async_write_ queue will be empty for the current Tensix core.

Return value: None



#### noc_async_write

template<uint32_t max_page_size = NOC_MAX_BURST_SIZE + 1>  
inline void noc_async_write(std::uint32_t src_local_l1_addr, std::uint64_t
dst_noc_addr, std::uint32_t size, uint8_t noc = noc_index)  

    

Initiates an asynchronous write from a source address in L1 memory on the
Tensix core executing this function call. The destination is specified using a
uint64_t encoding referencing an on-chip node located at NOC coordinates (x,y)
and a local address created using get_noc_addr function. Also, see
_noc_async_write_barrier_.

The destination node can be either a DRAM bank, Tensix core+L1 memory address
or a PCIe controller.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
src_local_l1_addr  | Source address in local L1 memory  | uint32_t  | 0..1MB  | True   
dst_noc_addr  | Encoding of the destination NOC location (x,y)+address  | uint64_t  | DOX-TODO (insert a reference to what constitutes valid coords)  | True   
size  | Size of data transfer in bytes  | uint32_t  | 0..1MB  | True 



#### noc_semaphore_wait

void noc_semaphore_wait(volatile uint32_t *sem_addr, uint32_t val)  

    

A blocking call that waits until the value of a local L1 memory address on the
Tensix core executing this function becomes equal to a target value. This L1
memory address is used as a semaphore of size 4 Bytes, as a synchronization
mechanism. Also, see _noc_semaphore_set_.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
sem_addr  | Semaphore address in local L1 memory  | uint32_t  | 0..1MB  | True   
val  | The target value of the semaphore  | uint32_t  | Any uint32_t value  | True 



### Other
#### get_common_arg_addr

static uint32_t get_common_arg_addr(int arg_idx)  

    

Returns the address in L1 for a given runtime argument index for common (all
cores) runtime arguments set via SetCommonRuntimeArgs() API.

Return value: Associated L1 address of given common runtime argument index

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
arg_idx  | Common Runtime argument index  | uint32_t  | 0 to 255  | True 



#### get_common_arg_val

template<typename T>  
T get_common_arg_val(int arg_idx)  

    

Returns the value at a given runtime argument index for common (all cores)
runtime arguments set via SetCommonRuntimeArgs() API.

Return value: The value associated with the common runtime argument index

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
arg_idx  | Common Runtime argument index  | uint32_t  | 0 to 255  | True   
T (template argument)  | Data type of the returned argument  | Any 4-byte sized type  | N/A  | True 



#### get_compile_time_arg_val

get_compile_time_arg_val(arg_idx)  

    

Returns the value of a constexpr argument from kernel_compile_time_args array
provided during kernel creation using CreateKernel calls.

Return value: constexpr uint32_t

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
arg_idx  | The index of the argument  | uint32_t  | 0 to 31  | True 



#### Kernel Argument APIs

  * [get_arg_addr](get_arg_addr.html)
  * [get_arg_val](get_arg_val.html)
  * [get_common_arg_addr](get_common_arg_addr.html)
  * [get_common_arg_val](get_common_arg_val.html)
  * [get_compile_time_arg_val](get_compile_time_arg_val.html)



#### get_arg_addr

static uint32_t get_arg_addr(int arg_idx)  

    

Returns the address in L1 for a given runtime argument index for unique (per
core) runtime arguments set via SetRuntimeArgs() API.

Return value: Associated L1 address of given unique runtime argument index

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
arg_idx  | Unique Runtime argument index  | uint32_t  | 0 to 255  | True 



#### get_arg_val

template<typename T>  
T get_arg_val(int arg_idx)  

    

Returns the value at a given runtime argument index for unique (per-core)
runtime arguments set via SetRuntimeArgs() API.

Return value: The value associated with the unique runtime argument index

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
arg_idx  | Unique Runtime argument index  | uint32_t  | 0 to 255  | True   
T (template argument)  | Data type of the returned argument  | Any 4-byte sized type  | N/A  | True 



### Pack-Unpack Operations
#### pack_tile

template<bool out_of_order_output = false>  
void ckernel::pack_tile(uint32_t ifrom_dst, uint32_t icb, std::uint32_t
output_tile_index = 0)  

    

Copies a single tile from the DST register buffer at a specified index to a
specified CB at a given index. For the out_tile_index to be valid for this
call, cb_reserve_back(n) has to be called first to reserve at least some
number n > 0 of tiles in the output CB. out_tile_index = 0 then references the
first tile in the reserved section of the CB, up to index n - 1, which will
then be visible to the consumer in the same order after a cb_push_back call.
The DST register buffer must be in acquired state via _acquire_dst_ call. This
call is blocking and is only available on the compute engine.

Each subsequent pack call will increment the write pointer in the cb by single
tile size. The pointer is then again set to a valid position with space for n
reserved tiles by another cb_reserve_back call.

Operates in tandem with functions cb_reserve_back and cb_push_back.

A typical use case is first the producer ensures that there is a number of
tiles available in the buffer via cb_reserve_back, then the producer uses the
pack_tile call to copy a tile from one of DST slots to a slot in reserved
space and finally cb_push_back is called to announce visibility of the
reserved section of the circular buffer to the consumer.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
ifrom_dst  | The index of the tile in the DST register  | uint32_t  | Must be less than the size of the DST register (16)  | True   
icb  | The identifier of the output circular buffer (CB)  | uint32_t  | 0 to 31  | True   
icb_tile  | The index of the tile in the output CB to copy to  | uint32_t  | Must be less than the size of the CB  | True   
  
void ckernel::matmul_pack_tile(uint32_t ifrom_dst, uint32_t icb, uint32_t
ntiles)  

    

Copies a block of tiles from the DST register buffer at a start index to a
specified CB at a given start index. cb_reserve_back(n) had to be called first
to reserve at least some number n>0 of tiles in the output CB. The
out_tile_index = 0 then references the first tile in the reserved section of
the CB, up to index n-1 that will then be visible to the consumer in the same
order after a cb_push_back call. The DST register buffer must be in acquired
state via _acquire_dst_ call. This call is blocking and is only available on
the compute engine.

Each subsequent pack call will increment the write pointer in the cb by ntiles
size. The pointer is then again set to a valid position with space for n
reserved tiles by another cb_reserve_back call.

Operates in tandem with functions cb_reserve_back and cb_push_back.

A typical use case is first the producer ensures that there is a number of
tiles available in the buffer via cb_reserve_back, then the producer uses the
matmul_pack_tile call to copy a block of tiles from the DST slots to the slots
in reserved space and finally cb_push_back is called to announce visibility of
the reserved section of the circular buffer to the consumer.

Return value: None

Argument  | Description  | Type  | Valid Range  | Required   
---|---|---|---|---  
ifrom_dst  | The index of the tile in the DST register  | uint32_t  | Must be less than the size of the DST register (16)  | True   
icb  | The identifier of the output circular buffer (CB)  | uint32_t  | 0 to 31  | True   
ntiles  | The number of tiles to copy from DST to CB  | uint32_t  | Must be less than the size of the CB  | True 



#### reconfig_data_format

template<bool to_from_int8 = false>  
void ckernel::reconfig_data_format(const uint32_t srca_new_operand, const
uint32_t srcb_new_operand)  

    

Helper function to reconfigure srca and srcb data formats.

template<bool to_from_int8 = false>  
void ckernel::reconfig_data_format(const uint32_t srca_old_operand, const
uint32_t srca_new_operand, const uint32_t srcb_old_operand, const uint32_t
srcb_new_operand)  

    

Helper function to reconfigure srca/srcb data formats, only if they differ
from existing formats.

template<bool to_from_int8 = false>  
void ckernel::reconfig_data_format_srca(const uint32_t srca_new_operand)  

    

Helper function to reconfigure srca data format.

template<bool to_from_int8 = false>  
void ckernel::reconfig_data_format_srca(const uint32_t srca_old_operand, const
uint32_t srca_new_operand)  

    

Helper function to reconfigure srca input data format, only if it differs from
existing format.

template<bool to_from_int8 = false>  
void ckernel::reconfig_data_format_srcb(const uint32_t srcb_new_operand)  

    

Helper function to reconfigure srcb input data format.

template<bool to_from_int8 = false>  
void ckernel::reconfig_data_format_srcb(const uint32_t srcb_old_operand, const
uint32_t srcb_new_operand)  

    

Helper function to reconfigure srcb input data format, only if it differs from
existing format.



#### Packing APIs

Packing and Unpacking APIs allow reinterpreting or construct/reading of
buffers as specific integer or floating point data types.

  * [pack_tile](pack_tile.html)
  * [reconfig_data_format](reconfig_data_format.html)



### SFPU Operations
#### Low Level Kernels

## Overview

SFPI is the programming interface to the SFPU. It consists of a C++ wrapper
around a RISCV GCC compiler base which has been extended with vector data
types and __builtin intrinsics to generate SFPU instructions. The wrapper
provides a C++ like interface for programming.

SFPI is supported on Grayskull and Wormhole.

## Compiler Options/Flags

The following flags must be specified to compile SFPI kernels:

    
    
    -m<arch> -fno-exceptions
    

where `arch` is one of:

>   * grayskull
>
>   * wormhole
>
>

Note that the arch specification above overrides any `-march=<xyz>` to either
`-march=rv32iy` for grayskull or `-march=rv32iw` for wormhole.

Further, the following options disable parts of the SFPI enabled compiler:

>   * `-fno-rvtt-sfpu-warn`: disable sfpu specific warnings/errors
>
>   * `-fno-rvtt-sfpu-combine`: disable sfpu instruction combining
>
>   * `-fno-rvtt-sfpu-cc`: disable sfpu CC optimizations
>
>   * `-fno-rvtt-sfpu-replay`: disable sfpu REPLAY optimizations (wormhole
> only)
>
>

### Example

Before going into details, below is a simple example of SFPI code:

    
    
    void silly(bool take_abs)
    {
        // dst_reg[n] loads into a temporary LREG
        vFloat a = dst_reg[0] + 2.0F;
    
        // This emits a load, move, mad (on GS uses the "+/0 .5" feature of MAD)
        dst_reg[3] = a * -dst_reg[1] + vConst0p6929 + 0.5F;
    
        // This emits a load, loadi, mad (a * dst_reg[] goes down the mad path)
        dst_reg[4] = a * dst_reg[1] + 1.2F;
    
        // This emits two loadis and a mad
        dst_reg[4] = a * 1.5F + 1.2F;
    
        // This emits a loadi (into tmp), loadi (as a temp for 1.2F) and a mad
        vFloat tmp = s2vFloat16a(value);
        dst_reg[5] = a * tmp + 1.2F;
    
        v_if ((a >= 4.0F && a < 8.0F) || (a >= 12.0F && a < 16.0F)) {
            vInt b = exexp_nodebias(a);
            b &= 0xAA;
            v_if (b >= 130) {
                dst_reg[6] = setexp(a, 127);
            }
            v_endif;
        } v_elseif (a == s2vFloat16a(3.0F)) {
            // RISCV branch
            if (take_abs) {
                dst_reg[7] = abs(a);
            } else {
                dst_reg[7] = a;
            }
        } v_else {
            vInt exp = lz(a) - 19;
            exp = ~exp;
            dst_reg[8] = -setexp(a, exp);
        }
        v_endif;
    }
    

The main things to note from the example are:

>   * Constants are expressed as scalars but are expanded to the width of the
> vector
>
>   * `v_if` (and related) predicate execution of vector operations such that
> only enabled vector elements are written
>
>   * The compiler views `v_if` and `v_elseif` as straight-line code, ie, both
> sides of the conditionals are executed
>
>   * RISCV conditional and looping instructions work as expected (only one
> side executed)
>
>   * Math expressions for vectors work across all enabled vector elements
>
>   * Presently, `v_endif` is required to close out all
> `v_if`/`v_elseif`/`v_else` chains
>
>

## Details

### Namespace

All the data types/objects/etc. listed below fall within the `sfpi` namespace.

### User Visible Data Types

The following data types are visible to the programmer:

>   * `vFloat`
>
>   * `vInt`
>
>   * `vUInt`
>
>   * enum `LRegs`
>
>

Each of the `v` types is a strongly typed wrapper around the weakly typed
compiler data type `__rvtt_vec_t`. On Grayskull this is a vector of 64 19 bit
values while on Wormhole this is a vector of 32 32 bit values.

LRegs are the SFPU’s general purpose vector registers. `LRegs` enumerates
these registers.

#### User Visible Constants

Constant registers are implemented as objects which can be referenced wherever
a vector can be used.

>   * Grayskull:
>
>     * `vConst0`
>
>     * `vConst0p6929`
>
>     * `vConstNeg1p0068`
>
>     * `vConst1p4424`
>
>     * `vConst0p8369`
>
>     * `vConstNeg0p5`
>
>     * `vConst1`
>
>     * `vConstNeg1`
>
>     * `vConst0p0020`
>
>     * `vConstNeg0p6748`
>
>     * `vConstNeg0p3447`
>
>     * `vConstTileId`, enumerates the vector elements: [0..63]
>
>

  * Wormhole:

    * `vConst0`

    * `vConst1`

    * `vConst0p8373`

    * `vConstNeg1`

    * `vConstTileId`, counts by two through the vector elements: [0, 2, 4..62]

    * `vConstFloatPrgm0`, `vConstIntPrgm0`

    * `vConstFloatPrgm1`, `vConstIntPrgm1`

    * `vConstFloatPrgm2`, `vConstIntPrgm2`

#### User Visible Objects

>   * `dst_reg[]` is an array used to access the destination register
>
>   * `l_reg[]` is an array used to load/store to specific SFPU registers
>
>

#### Macros

The only macros used within the wrapper implement the predicated conditional
processing mechanism. These (of course) do not fall within the SFPI namespace
and for brevity run some chance of a namespace collision. They are:

>   * `v_if()`
>
>   * `v_elseif()`
>
>   * `v_else`
>
>   * `v_endif`
>
>   * `v_block`
>
>   * `v_endblock`
>
>   * `v_and()`
>
>

The conditionals work mostly as expected but note the required `v_endif` at
the end of an if/else chain. Forgetting this results in compilation errors as
the `v_if` macro contains a `{` which is matched by the `v_endif`.

`v_block` and `v_and` allow for the following code to progressively “narrow”
the CC state:

    
    
    v_block {
        for (int x = 0; x < n; x++) {
            v1 = v1 - 1;
            v_and (v1 >= 0);
            v2 *= 2;
        }
    }
    v_endblock;
    

`v_and` can be used inside any predicated conditional block (i.e., a `v_block`
or a `v_if`).

### Data Type Details

#### vFloat

>   * Assignment: from float, dst_reg[n]
>
>   * Conversion: `reinterpret<AnotherVecType>()` converts, in place, between
> vInt and vUInt and vFloat
>
>   * Immediate loads: see section **Immediate Floating Point Values** below
>
>   * Operators: `+`/`-`/`*` should work as expected with dst_reg[n], vFloat
> and vConst
>
>   * Conditionals: all 6 (`<`, `<=`, `==`, `!=`, `>=`, `>`) are supported.
> Note that `<=` and `>` pay a performance penalty relative to the others
>
>

#### vInt

>   * Assignment: from integer, dst_reg[n]
>
>   * Conversion: `reinterpret<AnotherVecType>()` converts, in place, between
> vFloat and vUInt
>
>   * Operators: `&`, `&=`, `|`, `|=`, `~`, `^`, `^=`, `<<` and `+`, `-`,
> `+=`, `-=`, `++`, `--`. (there is no signed right shift on Grayskull or
> Wormhole)
>
>   * Conditionals: all 6 (`<`, `<=`, `==`, `!=`, `>=`, `>`) are supported.
> Note that `<=` and `>` pay a performance penalty relative to the others
>
>

#### vUInt

>   * Assignment: from unsigned integer, dst_reg[n]
>
>   * Conversion: `reinterpret<AnotherVecType>()` converts, in place, between
> vFloat and vInt
>
>   * Operators: `&`, `&=`, `|`, `|=`, `~`, `^`, `^=`, `<<`, `>>` and `+`,
> `-`, `+=`, `-=`, `++`, `--`
>
>   * Conditionals: all 6 (`<`, `<=`, `==`, `!=`, `>=`, `>`) are supported.
> Note that `<=` and `>` pay a performance penalty relative to the others
>
>

Note that on Wormhole, the destination register format is always determined by
the run time. So, for example, reading a vInt when the format is set to
float32 gives unexpected results.

### Library

Below `Vec` means any vector type.

Below is a list of library calls, further documentation is below.

#### Grayskull and Wormhole

    
    
    vInt exexp(const vFloat v)
    vInt exexp_nodebias(const vFloat v)
    

Extracts, optionally debiases and then returns the 8-bit exponent in ‘’v’’ in
bits 7:0.

    
    
    vInt exman8(const vFloat v)
    vInt exman9(const vFloat v)
    

Extracts and returns the mantissa of v. ‘’exman8’’ adds the hidden bit and
pads the left side with 8 zeros while ‘’exman9’ does not include the hidden
bit and pads the left side with 9 zeros.

    
    
    vFloat setexp(const vFloat v, const uint32_t exp)
    vFloat setexp(const vFloat v, const Vec[U]Short exp)
    

Replaces the exponent of ‘’v’’ with the exponent in bits 7:0 of ‘’exp’’ and
returns the result (preserving the sign and mantissa of ‘’v’’).

    
    
    vFloat setman(const vFloat v, const uint32_t man)
    vFloat setman(const vFloat v, const Vec[U]Short man) // This does not work on GS due to a HW bug
    

Replaces the mantissa of ‘’v’’ with the mantissa in the low bits of ‘’man’’
and returns the result (preserving the sign and exponent of ‘’v’’).

    
    
    vFloat setsgn(const vFloat v, const int32_t sgn)
    vFloat setsgn(const vFloat v, const vFloat sgn)
    vFloat setsgn(const vFloat v, const vInt sgn)
    

Replaces the sign bit of ‘’v’’ with the sign in ‘’sgn’’ and returns the result
(preserving the exponent and mantissa of ‘’v’’). Note that the ‘’int32_t’’
version takes the sign from bit 0 while the ‘’vFloat’’ and ‘’vInt’’ versions
take the sign from the sign bit location (bit 19 on GS and bit 32 on WH).

    
    
    vFloat addexp(const vFloat v, const int32_t exp)
    

Adds the 8-bit value in ‘’exp’’ to the exponent of ‘’v’’ and returns the
result (preserving the sign and mantissa of ‘’v’’).

    
    
    vFloat lut(const vFloat v, const vUInt l0, const vUInt l1, const vUInt l2, const int offset)
    vFloat lut_sign(const vFloat v, const vUInt l0, const vUInt l1, const vUInt l2, const int offset)
    

‘’l0’’, ‘’l1’’, ‘’l2’’ each contain 2 8-bit floating point values ‘’A’’ and
‘’B’’ with ‘’A’’ in bits 15:8 and ‘’B’’ in bits 7:0. The 8-bit format is:

    

  * 0xFF represents the value 0, otherwise

  * bit[7] is the sign bit, bit[6:4] is the unsigned exponent_extender and bit[3:0] is the mantissa

Floating point representations of ‘’A’’ and ‘’B’’ (19-bit on GS and 32-bit on
WH) are constructed by:

    

  * Using the sign bit

  * Generating an 8-bit exponent as (127 – exponent_extender)

  * Generating a mantissa by padding the right of the specified 4 bit mantissa with 0s

‘’A’’ and ‘’B’’ are selected from one of ‘’l0’’, ‘’l1’’ or ‘’l2’’ based on the
value in ‘’v’’ as follows:

    

  * ‘’l0’’ when ‘’v’’ < 0

  * ‘’l1’’ when ‘’v’’ == 0

  * ‘’l2’’ when ‘’v’’ > 0

XXXX is this backwards? Returns the result of the computation ‘’A * ABS(v) +
B’’. The ‘’lut_sgn’’ variation discards the calculated sign bit and instead
uses the sign of ‘’v’’.

    
    
    vInt lz(Vec v)
    

Returns the count of leading (left-most) zeros of ‘’v’’.

    
    
    vFloat abs(vFloat v)
    vInt abs(vInt v)
    

Returns the absolute value of ‘’v’’.

    
    
    vUInt shft(const vUInt v, const vInt amt)
    

Performs a left shift (when ‘’amt’’ is positive) or right shift (when ‘’amt’’
is negative) of ‘’v’’ by ‘’amt’’ bits.

#### Wormhole only

    
    
    void vec_swap(Vec& A, Vec& B)
    

Swaps the (integer or floating point) vectors in ‘’A’’ and ‘’B’’.

    
    
    void vec_min_max(Vec& min, Vec& max)
    

Compares and swaps each element of the two vectors such that on return ‘’min’’
contains all of the minimum values and ‘’max’’ contains all of the maximum
values.

    
    
    Vec subvec_shflror1(Vec& v)
    Vec subvec_shflshr1(Vec& v)
    
    
    
    void subvec_transp(Vec& A, Vec& B, Vec& C, Vec& D)
    
    
    
    vInt lz_nosgn(const Vec v)
    

Returns the count of leading (left-most) zeros of ‘’v’’ ignoring the sign bit.

    
    
    vFloat int_to_float(vInt in, int round_mode = 1)
    vUInt float_to_fp16a(vFloat in, int round_mode = 1)
    vUInt float_to_fp16b(vFloat in, int round_mode = 1)
    vUInt float_to_uint8(vFloat in, int round_mode = 1)
    vUInt float_to_int8(vFloat in, int round_mode = 1)
    vUInt int32_to_uint8(vInt in, vUInt descale, int round_mode = 1)
    vUInt int32_to_uint8(vInt in, unsigned int descale, int round_mode = 1)
    vUInt int32_to_int8(vInt in, vUInt descale, int round_mode = 1)
    vUInt int32_to_int8(vInt in, unsigned int descale, int round_mode = 1)
    vUInt float_to_uint16(vFloat in, int round_mode = 1)
    vUInt float_to_int16(vFloat in, int round_mode = 1)
    

Returns the rounded value performing round-to-even when ‘’round_mode’’ is 0
and stochastic rounding when ‘’round_mode’’ is 1.

### Immediate Floating Point Values

Assigning a float to a vFloat behaves slightly different on Grayskull vs
Wormhole. On Grayskull, the value is interpreted as an fp16b; use the
conversion routines below to explicitly specify the format. On Wormhole, the
floating point value is converted to an fp16a, fp16b, or fp32 by first looking
to see if the range fits in fp16b and if not using fp16a (or fp32). If the
value is not known at compile time, then it is loaded as an fp32. Note that on
Wormhole fp32 loads take 2 cycles.

For more explicit conversions, use one of the classes `s2vFloat16a` and
`s2vFloat16b`. Each takes either an integer or floating point value. Floating
point immediate values are converted at compilation time and incur no
overhead. Floating point variables that are not known at compilation time are
converted at run time. An integer value loaded into floating point vector (via
one of the conversion routines) is treated as a bit pattern and incurs no
overhead, see examples below.

Note: fp16a conversions do not presently handle denorms/nans, etc. properly.

Example uses:

    
    
    vFloat x = 1.0f;               // Load fb16b value
    vFloat x = 500000.0f;          // GS load fp16b value, WH fp32 value
    vFloat x = s2vFloat16a(3.0F);  // Load fp16a value, no overhead
    unsigned int ui = 0x3c00;
    vFloat x = s2vFloat16a(ui);    // Load fp16a value (1.0F), no overhead
    float f = 1.0F;
    vFloat x = s2vFloat16a(f);     // Load fp16a value, overhead if value cannot be determined at compile time
    

#### Boolean Operators

All conditionals operating on base types can be combined with any of `&&`,
`||`, `!`.

#### vBool

`vBool` doesn’t exist yet, but the functionality can be obtained by executing
conditional instructions outside of a `v_if` and assigning the result to a
`vInt`. This can be useful to, e.g., use RISCV code to conditionally generate
an SFPU predicate. For example, the following function evaluates different
predicated conditionals based on the value of a function parameter:

    
    
    sfpi_inline vInt sfpu_is_fp16_zero(const vFloat& v, uint exponent_size_8)
    {
        if (exponent_size_8) {
            return v == 0.0F;
        } else {
            vInt tmp = 0x3800; // loads {0, 8'd112, 10'b0}
            tmp += reinterpret<vInt>(v);
            return tmp == 0;
        }
    }
    

which may be called by:

    
    
    v_if (sfpu_is_fp16_zero(v, exponent_size_8)) {
        ...
    }
    v_endif;
    

If exponent_size_8 is known at compile time, this has no overhead. If not, the
predication is determined at runtime.

#### Assigning and Using Constant Registers

Programmable constant registers (Wormhole only) are accessed and assigned just
like any other variables, for example:

    
    
    vConstFloatPrgm0 = 3.14159265;
    vFloat two_pi = 2.0f * vConstFloatPrgm0;
    

Writing to a constant register first loads the constant into a temporary LReg
then assigns the LReg to the constant register and so takes 1 cycle longer
than just loading an LReg. Accessing a constant register is just as fast as
accessing an LReg. Loading a constant register loads the same value into all
vector elements.

#### Assigning LRegs

Some highly optimized code may call a function prior to the kernel to pre-load
values into specific LRegs and then access those values in the kernel. Note
that if the register’s value must be preserved when the kernel exits, you must
restore the value explicitly by assigning back into the LReg.

For example:

    
    
    vFloat x = l_reg[LRegs::LReg1];  // x is now LReg1
    vFloat y = x + 2.0f;
    l_reg[LRegs::LReg1] = x;         // this is necessary at the end of the function
                                     // to preserve the value in LReg1 (if desired)
    

## Miscellaneous

### Register Pressure Management

Note that the wrapper introduces temporaries in a number of places. For
example:

    
    
    dst_reg[0] = dst_reg[0] + dst_reg[1];
    

loads dst_reg[0] and dst_reg[1] into temporary LREGs (as expected).

The compiler will not spill registers. Exceeding the number of registers
available will result in the cryptic: `error: cannot store SFPU register
(reigster spill?) - exiting!` without a line number.

The compiler does a reasonable job with lifetime analysis when assigning
variables to registers. Reloading or recalculating results helps the compiler
free up and re-use registers and is a good way to correct a spilling error.

Grayskull has 4 general purpose LRegs, Wormhole has 8.

### Optimizer

There is a basic optimizer in place. The optimization philosophy to date is to
enable the programmer to write optimal code. This is different from mainstream
compilers which may generate optimal code given non-optimal source. For
example, common sub-expression elimination and the like are not implemented.
The optimizer will handle the following items:

>   * MAD generation (from MUL/ADD)
>
>   * MULI, ADDI generation (from MUL + const, or ADD + const)
>
>   * Adding a 0.5f to the end of ADD/MULL/MAD/MULI/ADDI (Grayskull only)
>
>   * Swapping the order of arguments to instructions that use the
> destination-as-source, e.g., SFPOR to minimize the need for register moves
>
>   * CC enables (PUSHC, POPC, etc.)
>
>   * Instruction combining for comparison operations. For example, a subtract
> of 5 followed by a compare against 0 gets combined into one operation
>
>   * Wormhole only: NOP insertion for instructions which must be followed by
> an independent instruction or NOP. Note that this pass (presently) does not
> move instructions to fill the slot but will skip adding a NOP if the next
> instruction is independent. In other words, reordering your code to reduce
> dependent chains of instructions may improve performance
>
>

There is a potential pitfall in the above in that the MAD generator could
change code which would not run out of registers with, say, a MULI followed by
an ADDI into code that runs out of registers with a MAD. (future todo to fix
this).

### SFPREPLAY

The `SFPREPLAY` instruction available on Wormhole allows the RISCV processor
to submit up to 32 SFP instructions at once. The compiler looks for sequences
of instructions that repeat, stores these and then “replays” them later.

The current implementation of this is very much first cut: it does not handle
kernels with rolled up loops very well. Best performance is typically attained
by unrolling the top level loop and then letting the compiler find the
repetitions and replace them with `SFPREPLAY`. This works well when the main
loop contains < 32 instructions, but performance starts to degrade again as
the number of instructions grows (future work).

The other issue that can arise with `SFPREPLAY` is that sometimes the last
unrolled loop of instructions uses different registers than the prior loops
resulting in imperfect utilization of the replay.

### Emulation

There is an emulator for the SFPU that works at the __builtin level.
Compilation and runtime are extremely fast (sub 1 second) so this may be
useful during development.

Look in the file main.cc in the `sfpi` submodule under `src/ckernels`, there
is an example kernel there to lead the way.

The main difference between compilation and running on HW is that the emulator
has an infinite number of registers and so code that runs there may fail on
the HW due to spilling. The `Makefile` builds for both rv32 (generating a `.S`
file) and x86 (to run through emulation) and so an “out of registers” message
for rv32 tells you you have work to do.

The emulator for WH is not fully implemented (missing some of the new WH
specific instructions)

### Tools

The sfpi submodule contains a `tools` directory. `cd` into that directory and
type `make` to build `fp16c` which is a converter that converts floating point
values to fp16a, fp16b and the LUT instruction’s fp8 as well as the other way
(integer to float/fp16a/fp16b/fp8). This is useful for writing optimal code or
looking through assembly dumps.

## Pitfalls/Oddities/Limitations

### Arrays/Storing to Memory

The SFPU can only read/write vectors to/from the destination register, it
cannot read/write them to memory. Therefore, SFPI does not support arrays of
vectors. Using arrays may work if the optimizer is able to optimize out the
loads/stores, however, this is brittle and so is not recommended. Storing a
vector to memory will result in an error similar to the following:

    
    
    tt-metal/tt_metal/hw/ckernels/sfpi/include/sfpi.h:792:7: error: cannot write sfpu vector to memory
      792 |     v = (initialized) ? __builtin_rvtt_sfpassign_lv(v, in) : in;
          |       ^
    /tt-metal/tt_metal/hw/ckernels/sfpi/include/sfpi.h:792:7: error: cannot write sfpu vector to memory
    

### Function Calls

There is no ABI and none of the vector types can be passed on the stack.
Therefore, all function calls must be inlined. To ensure this use
`sfpi_inline`, which is defined to `__attribute__((always_inline))` on GCC.

### Register Spilling

The compiler does not implement register spilling. Since Grayskull only has 4
LRegs, running out of registers is a common occurrence. If you see the
following: `error: cannot store SFPU register (reigster spill?) - exiting!`
you have most likely run out of registers.

### Error Messages

Unfortunately, many errors are attributed to the code in the wrapper rather
than in the code being written. For example, using an uninitialized variable
would show an error at a macro called by a wrapper function before showing the
line number in the user’s code.

### Limitations

>   * Forgetting a `v_endif` results in mismatched {} error which can be
> confusing (however, catches the case where a `v_endif` is missing!)
>
>   * In general, incorrect use of vector operations (e.g., accidentally using
> a scalar argument instead of a vector) results in warnings/errors within the
> wrapper rather than in the calling code
>
>   * Keeping too many variables alive at once (4 on GS) requires register
> spilling which is not implemented and causes a compiler abort
>
>   * The gcc compiler occasionally moves a value from one register to another
> for no apparent reason. At this point it appears there is nothing that can
> be done about this besides hoping that the issue is fixed in a future
> version of gcc.
>
>