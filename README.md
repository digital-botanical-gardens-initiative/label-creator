# label-creator

[![Release](https://img.shields.io/github/v/release/edouardbruelhart/label-creator)](https://img.shields.io/github/v/release/edouardbruelhart/label-creator)
[![Build status](https://img.shields.io/github/actions/workflow/status/edouardbruelhart/label-creator/main.yml?branch=main)](https://github.com/edouardbruelhart/label-creator/actions/workflows/main.yml?query=branch%3Amain)
[![Commit activity](https://img.shields.io/github/commit-activity/m/edouardbruelhart/label-creator)](https://img.shields.io/github/commit-activity/m/edouardbruelhart/label-creator)

- **Github repository**: <https://github.com/edouardbruelhart/label-creator/>

### Features

Label Creator software permits to create all sorts of labels for the EMI project.

- It requests the Directus database, generates labels (field samples, mobile containers and static containers) asked by the user and reserves them. Then it formats them in pdf format to fit [avery L4732](https://www.avery.co.uk/product/mini-multipurpose-labels-l4732rev-25) labels, ready to print.

- It also generates labels from a CSV table, without adding them to Directus. This mode is made to easily print provisory labels or labels that don't fit EMI requiremnts.

- Finally it also permits to add universities to the Directus database in order to track samples across different institutions.

### How to use:

- **Windows:** Simply download the `.exe` binary from the `Releases` tab and run it.
- **Linux:** Download the `linux` binary from the `Releases` tab, then add execution rights:

  ```bash
  sudo chmod +x label_creator_vxx_linux
  ```

  It will then be executable. If you want to run it from the command line, you can simply move it to a folder in the PATH (e.g., `/usr/local/bin`). Then you just need to type:

  ```bash
  label_creator_vxx_linux
  ```

  in bash.

- **MacOS:** Download the `MacOS` binary from the `Releases` tab, then add execution rights:

  ```bash
  sudo chmod +x label_creator_vxx_macos
  ```

  It will then be executable. If you want to run it from the command line, you can simply move it to a folder in the PATH. Then you just need to type:

  ```bash
  label_creator_vxx_macos
  ```

  in the terminal.

- **General method:** Clone the project, then set up an environment with `poetry`:

  ```bash
  poetry install
  ```

  Then activate the environment:

  ```bash
  poetry shell
  ```

  and run the `label_creator.py` script:

  ```bash
  python label_creator.py
  ```

  If you do not have poetry, you can install it with the command:

  ```bash
  pipx install poetry
  ```
