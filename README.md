# Braille Phonics Plus – Firmware

## 📌 Project Description

Firmware for the Braille Phonics Plus system developed for our thesis.
This project runs on a Raspberry Pi and interfaces with hardware modules for testing and development of assistive learning features.

## 🛠 Hardware Used

* Raspberry Pi
* TCA I2C Module (e.g., TCA9548A)
* Connected I2C peripherals (for testing)

## ⚙️ Setup Instructions

1. Clone the repository:

```
git clone https://github.com/executeshawn/braillephonics-plus-fw.git
cd braillephonics-plus-fw
```

2. Create virtual environment:

```
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```
pip install -r requirements.txt
```

4. Run test script:

```
python tca_test.py
```

## 🔁 Recreating the Virtual Environment

The `venv/` folder is intentionally excluded from this repository.
To recreate it:

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

Developed for thesis implementation and hardware testing.
