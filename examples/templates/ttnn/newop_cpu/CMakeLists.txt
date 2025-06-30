add_library(ttnn_op_experimental_new_op ${LIB_TYPE})
add_library(TTNN::Ops::Experimental::NewOp ALIAS ttnn_op_experimental_new_op)

target_precompile_headers(ttnn_op_experimental_new_op REUSE_FROM TT::CommonPCH)
TT_ENABLE_UNITY_BUILD(ttnn_op_experimental_new_op)

target_sources(
    ttnn_op_experimental_new_op
    PRIVATE
        new_op.cpp
        new_op_pybind.cpp
)

target_include_directories(ttnn_op_experimental_new_op PRIVATE ${FixmeOpIncDirs})
target_link_libraries(
    ttnn_op_experimental_new_op
    PRIVATE
        TT::Metalium
        TTNN::Core
)

install(TARGETS ttnn_op_experimental_new_op LIBRARY COMPONENT tar)
