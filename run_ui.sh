#!/bin/bash
pytest tests/ui --headed
allure serve allure-results