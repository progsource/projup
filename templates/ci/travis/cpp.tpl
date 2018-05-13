dist: trusty
sudo: false
language: cpp
compiler: g++
install: export CXX="g++-6"
addons:
  apt:
    sources:
      - ubuntu-toolchain-r-test
    packages:
      - g++-6

script:
  - mkdir tmp
  - cd tmp
  - cmake ..
  - make
  - ../build/{technicalTitle}Tests
