<div style="display: flex; justify-content: center; align-items: center;">
  <img
    src="https://docs.arcade.dev/images/logo/arcade-logo.png"
    style="width: 250px;"
  >
</div>

<div style="display: flex; justify-content: center; align-items: center; margin-bottom: 8px;">
  <img src="https://img.shields.io/github/v/release/pmdroid/tessie" alt="GitHub release" style="margin: 0 2px;">
  <img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="Python version" style="margin: 0 2px;">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License" style="margin: 0 2px;">
  <img src="https://img.shields.io/pypi/v/tessie" alt="PyPI version" style="margin: 0 2px;">
</div>
<div style="display: flex; justify-content: center; align-items: center;">
  <a href="https://github.com/pmdroid/tessie" target="_blank">
    <img src="https://img.shields.io/github/stars/pmdroid/tessie" alt="GitHub stars" style="margin: 0 2px;">
  </a>
  <a href="https://github.com/pmdroid/tessie/fork" target="_blank">
    <img src="https://img.shields.io/github/forks/pmdroid/tessie" alt="GitHub forks" style="margin: 0 2px;">
  </a>
</div>


<br>
<br>

# Arcade Tessie Toolkit

Tesla vehicle management tools using the Tessie API for real-time monitoring and control.

> **Note:** This implementation is done with Tessie but can be easily changed to the Tesla Fleet API because the endpoints are the same - only the domain changes. See [Tessie's Tesla Fleet API access documentation](https://developer.tessie.com/reference/access-tesla-fleet-api) for more details.

## Tools

### Car Information
- `get_location(vin)` - Get current vehicle location
- `get_battery(vin)` - Get battery level and range

### Driver Management  
- `get_drivers(vin)` - List authorized drivers
- `delete_driver(vin, user_id)` - Remove driver access

### Invitation Management
- `list_invitation(vin)` - List active invitations
- `create_invitation(vin)` - Create sharing invitation
- `revoke_invitation(vin, invite_id)` - Cancel invitation

## Requirements

- `TESSIE_TOKEN` secret for API authentication

## Development

```bash
# Create env
uv venv --seed -p 3.13

# Activate the env
source .venv/bin/activate

# Install dependencies
make install

# Run tests
make test

# Run code quality checks
make check

# Generate coverage report
make coverage

# Build package
make build
```

## Local Testing

```bash
# Serve toolkit locally
arcade serve

# Serve with auto-reload
arcade serve --reload
```

## Deployment

```bash
# Deploy to Arcade cloud
arcade deploy

# Verify deployment
arcade worker list
```

## Evaluation

The toolkit includes comprehensive evaluation suites:
- `evals/eval_car.py` - Car functionality evaluations
- `evals/eval_drivers.py` - Driver management evaluations  
- `evals/eval_invitation.py` - Invitation management evaluations

Read the docs on how to create a toolkit [here](https://docs.arcade.dev/home/build-tools/create-a-toolkit)