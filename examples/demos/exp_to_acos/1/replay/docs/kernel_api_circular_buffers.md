### Circular Buffers
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

void cb_push_back(const int32_t operand, const int32_t num_pages)

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