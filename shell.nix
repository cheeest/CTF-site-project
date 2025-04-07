{ pkgs ? import <nixpkgs> {} }:
with pkgs; mkShell rec {
  buildInputs = [
    (python3.withPackages (ps: with ps; [
      flask
      flask_assets
      libsass
      setuptools
    ]))
  ];
}
