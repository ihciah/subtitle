# SubTitle

A cli tool to download subtitles. 

Different to others similar tools, this tool use video hash to match subtitles from Thunder Network subtitle database, which makes it accurate. 

Besides, the subtitle database of Thunder Network is contributed by a large number of users in China. So it can work fine for almost all movies.

### Features
- Download subtitles of given video file or folder from Thunder Network server using cli.
- Watch aria2 download directory, download subtitles automatically when task finished.
- DNS-over-HTTP is enabled by default considering network interference in some network(such as Fudan Campus Network).

### Install
You need `Python` and `pip` to run this tool.

You can download them from [Here](https://www.python.org/downloads/) if you don\'t have them. 
Both of `Python2.x` and `Python3.x` can work properly for this tool.

The newest `Python3.x` is recommended.

After the `Python` and `pip` are setup, you can simply run this command to install this tool:

```bash
pip install subtitle --upgrade
```

### Usage Example
```bash
sub movie.mkv
subtitle movie.mkv
sub movies_dir
sub -l aria2_download_dir
```
Run `sub -h` to see all usages.
