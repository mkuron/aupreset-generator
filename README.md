# Audio Unit Preset Generator

This script create .aupreset files for Audio Unit instruments from the factory preset database.
It currently supports the following instruments:

* Waldorf PPG Wave 3.V
* Arturia Analog Lab, V Collection instruments, Pigments

It is easily extended to other plugins (pull requests are welcome) as long as the presets are available in NKS format or an SQLite database.

## Usage

```bash
git clone https://github.com/mkuron/aupreset-generator.git
cd aupreset-generator
python3 -m pip install -r requirements.txt
python3 -m aupreset_generator
```

## Screenshots

### Waldorf PPG Wave 3.V

#### before

![PPG Wave 3.V without presets](docs/ppgwave_before.png)

#### after

![PPG Wave 3.V with presets](docs/ppgwave_after.png)

### Arturia Analog Lab 5

#### before

![Analog Lab 5 without presets](docs/analoglab_before.png)

#### after

![Analog Lab 5 with presets](docs/analoglab_after.png)
