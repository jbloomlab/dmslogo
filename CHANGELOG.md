# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com).

## 0.7.0

### Fixed
- Updated minimum Python version to 3.9

- Update tests to use Python 3.11 and run on GitHub Actions rather than Travis CI

- Require at least `matplotlib` version 3.8 and modify code to work with that version.

## 0.6.3

### Fixed
- Bypass error associated with loading some font files on Mac OS X.

## 0.6.2

### Fixed
- Problems with title placements introduced in 0.6.0.

## 0.6.1

### Added
- `alpha` argument to `ValueToColorMap.scale_bar`

## 0.6.0

### Added
- Added `colorschemes.ValueToColorMap`.
- Ability to add overlay color bars to `draw_logo` (`heatmap_overlays` arg).

## 0.5.1

### Added
- Added `min_upperlim` and `max_lowerlim` to `AxLimSetter`.

## 0.5.0

### Added
- Ability to shade stacks in `draw_logo`.

## 0.4.0

### Added
- Additional ways set y-axis limits. This involves adding `utils.AxLimSetter`, and adding the `ylim_setter` param to `draw_logo` / `draw_line`. It also involves enabling `set_ylims` in `facet_plot` to take per-row values. Finally, a new example on y-limit setting was added.
- Allow `show_color` for `draw_line` to be `None`.

### Fixed
- Updated how fontlist is built to fix [this matplotlib warning](https://github.com/matplotlib/matplotlib/issues/17568).
- Fixed deprecation warnings.

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

