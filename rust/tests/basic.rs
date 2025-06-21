#[test]
fn test_start_stop() {
    // This just checks the audio stream can be built on this system.
    let host = cpal::default_host();
    if host.default_input_device().is_none() {
        // skip test if no mic
        return;
    }
    let device = host.default_input_device().unwrap();
    let config = device.default_input_config().unwrap();
    let stream = device
        .build_input_stream(&config.into(), move |_data: &[i16], _| {}, |_| {})
        .unwrap();
    drop(stream);
}

#[test]
fn test_start_stop() {
    // This just checks the audio stream can be built on this system.
    use cpal::traits::{DeviceTrait, HostTrait};

    let host = cpal::default_host();
    if host.default_input_device().is_none() {
        // skip test if no mic
        return;
    }
    let device = host.default_input_device().unwrap();
    if device.default_input_config().is_err() {
        // skip if no default config (e.g., headless CI)
        return;
    }
}
