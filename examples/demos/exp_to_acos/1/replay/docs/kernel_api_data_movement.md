### Data Movement Operations

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