### Common Functions

#### Kernel Argument APIs

  * [get_arg_addr](get_arg_addr.html)
  * [get_arg_val](get_arg_val.html)
  * [get_common_arg_addr](get_common_arg_addr.html)
  * [get_common_arg_val](get_common_arg_val.html)
  * [get_compile_time_arg_val](get_compile_time_arg_val.html)

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