## Demo
 https://xkamson.github.io/workflow-builder-web/
 -----------------------------------------------

# Engineer's Thesis -- Marcin Kamiński
Web app for managing the machine learning process for Engineer's Thesis on AGH (University of Science and Technology) in Cracow.

[![Build Status](https://travis-ci.com/marcinxkaminski/workflow-builder-api.svg?branch=master)](https://travis-ci.com/marcinxkaminski/workflow-builder-api)
[![Known Vulnerabilities](https://snyk.io/test/github/marcinxkaminski/workflow-builder-api/badge.svg?targetFile=requirements.txt)](https://snyk.io/test/github/marcinxkaminski/workflow-builder-api?targetFile=requirements.txt)
[![codecov](https://codecov.io/gh/marcinxkaminski/workflow-builder-api/branch/master/graph/badge.svg)](https://codecov.io/gh/marcinxkaminski/workflow-builder-api)
[![Maintainability](https://api.codeclimate.com/v1/badges/1cbf74062eaec12256e9/maintainability)](https://codeclimate.com/github/marcinxkaminski/workflow-builder-api/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/1cbf74062eaec12256e9/test_coverage)](https://codeclimate.com/github/marcinxkaminski/workflow-builder-api/test_coverage)

### Prerequisites
 - Python 3.8

### Development

* Install
    ```
    pip install -r requirements.txt
    ```

* Run
    ```
    uvicorn server:app --reload --log-level debug --log-config logs/uvicorn.txt
    ```

### API Documentation
Available at: http://workflow-builder-api.herokuapp.com/docs
or if you're running dev (on localhost): http://localhost:8000/docs


### Authors
  * [Marcin Kamiński](https://github.com/xkamson)
