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