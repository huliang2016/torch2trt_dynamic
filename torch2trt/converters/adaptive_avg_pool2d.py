from torch2trt.torch2trt import *
from torch2trt.module_test import add_module_test
from torch2trt.plugins import create_adaptivepool_plugin


@tensorrt_converter('torch.nn.functional.adaptive_avg_pool2d')
def convert_adaptive_avg_pool2d(ctx):
    input = ctx.method_args[0]
    output_size = get_arg(ctx, 'output_size', pos=1, default=0)
    output = ctx.method_return
    input_trt = trt_(ctx.network, input)

    if isinstance(output_size, int):
        output_size = (output_size, output_size)
    
    output_size = tuple([-1 if not o else o for o in output_size])

    plugin = create_adaptivepool_plugin("adaptive_avg_pool2d_"+str(id(input)),
                                        output_size=output_size,
                                        pooling_type=trt.PoolingType.AVERAGE)
            
    layer = ctx.network.add_plugin_v2(
        inputs=[input_trt], plugin=plugin)

    output._trt = layer.get_output(0)

### old
# @tensorrt_converter('torch.nn.functional.adaptive_avg_pool2d')
# def convert_adaptive_avg_pool2d(ctx):
#     ctx.method_args = (torch.nn.AdaptiveAvgPool2d(ctx.method_args[1]), ctx.method_args[0])
#     convert_AdaptiveAvgPool2d(ctx)
