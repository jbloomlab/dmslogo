# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com).

## 0.3.2

### Fixed
- Fix bug in error checks when `x_col` isn't sequential sites.

## 0.3.1

### Changed
- Put the mid-line on logo plots from `draw_logo` with negative values on top of text.

## 0.3.0

### Added
- Negative values can be plotted using both `draw_logo` and `draw_line` (as well as `facet_plot`). A new example Jupyter notebook was added for such plotting.

### Added
- Example notebooks now run on `mybinder`.

### Changed
- Examples now in Jupyter notebooks and converted to docs via `nbpshinx`.
- Tests now run on Python 3.7 as well as 3.6.
- Some improvements to docs.

## 0.2.3

### Added
- Option to fix y-limits in `facet_plot`.

## 0.2.2

### Changed
- Left and right margins now absolute rather than relative for `facet_plot`.
- Adjusted default width of plots created by `draw_logo`.

## 0.2.1

### Added
- Parameters to set better margins for `facet_plot`.
- Enable customization of underline colors in `draw_line`.

## 0.2.0

### Changed
- Better letter sizing in logo plots by adding manually adjusted fonts as package data, and changing how font scaling and spacing are done.

## 0.1.2

### Added
- Added `share_ylim_across_rows` to `facet_plot` to allow rows to have different y-limits.

## 0.1.1

### Added
- Enable `facet_plot` to facet rows that are missing an entry.

## 0.1.0
Initial release

