from torchlm.models import pipnet
# will auto download pretrained weights from latest release if pretrained=True
model = pipnet(backbone="resnet18", pretrained=True, num_nb=10, num_lms=98, net_stride=32,
               input_size=256, meanface_type="wflw", backbone_pretrained=True)
model.apply_freezing(backbone=True)
model.apply_training(
    annotation_path="/home/ailab/ai_code/Face/torchlm/data/WFLW/converted/train.txt",  # or fine-tuning your custom data
    num_epochs=10,
    learning_rate=0.0001,
    save_dir="./save/pipnet",
    save_prefix="pipnet-wflw-resnet18",
    save_interval=10,
    logging_interval=1,
    device="cuda",
    coordinates_already_normalized=True,
    batch_size=32,
    num_workers=4,
    shuffle=True
)

#/home/ailab/Downloads/WFLW_images
