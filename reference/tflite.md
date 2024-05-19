
## Notes
https://docs.ultralytics.com/guides/coral-edge-tpu-on-raspberry-pi/#prerequisites 
## Ultralytics Docs Summary
[Raspberry Pi with Coral Edge TPU](https://docs.ultralytics.com/guides/coral-edge-tpu-on-raspberry-pi/#installation-walkthrough)
1. Install, replace, or update Edge TPU Runtime with instructions and links to runtimes
2. Export any `model.pt` to edgetpu format
3. Terrible example of how to run inference with the new model
4. A confusing warning about why to run edge tpu model with `tflite-runtime` and not `tensorflow`. 

## How it actually should be:
1. Uninstall existing conflicts: 
    - pip package `tensorflow`
    - Edge TPU Runtimes from coral (has to do with plugging in tpu after installation)
2. Install ultralytics
3. Install OS depenent Edge TPU runtime
4. Connect Edge TPU to USB 3.0 port. This is because, according to the official guide, a new udev rule needs to take effect after installation. 
5. Export any `model.pt` to a Edge TPU formatted model with ultralytics or similar.

## Exporting for Edge TPU
[How to export to Edge TPU formatted model](https://docs.ultralytics.com/guides/coral-edge-tpu-on-raspberry-pi/#export-your-model-to-a-edge-tpu-compatible-model):

1. Requirments: Ultralytics, [Edge TPU Compiler](https://coral.ai/docs/edgetpu/compiler/) (distinct from runtime, and is not available on ARM)
2. Run following code to export:

    ```python
    from ultralytics import YOLO

    # Load a model
    model = YOLO('path/to/model.pt')  # Load a official model or custom model

    # Export the model
    model.export(format='edgetpu')
    ````

How to run TPU model with Ultralytics:
1. Install OS dependent Edge TPU runtime
2. Connect Edge TPU to USB3 port to trigger new `udev` rule
3. Run inference: 
    ```python
    from ultralytics import YOLO

    # Load the exported TFLite Edge TPU model
    edgetpu_model = YOLO('yolov8n_full_integer_quant_edgetpu.tflite')

    # Run TPU inference, probably still need object detection API for object detection
    results = edgetpu_model('https://ultralytics.com/images/bus.jpg')
    ```

## Coral Docs
[Edge TPU Compiler](https://coral.ai/docs/edgetpu/compiler/#compiler-and-runtime-versions)

Check compiler version:

`edgetpu_compiler --version`

Check runtime version on your device:

`python3 -c "import pycoral.utils.edgetpu; print(pycoral.utils.edgetpu.get_runtime_version())"`

[Edge TPU Model Requirements](https://coral.ai/docs/edgetpu/models-intro/#model-requirements)