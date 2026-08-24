# Flickr 照片元数据采集器

这是一个基于 Flickr API 的 Python 脚本：按关键词搜索照片，获取照片原图尺寸、拍摄日期、作者信息、照片地理位置和作者资料中的位置，并将结果保存到 SQLite 数据库。

## 功能

- 按关键词搜索 Flickr 照片
- 支持拍摄日期范围、每页数量和安全搜索
- 获取照片地理标签及作者公开资料中的位置/国家
- 获取可用的最大尺寸图片 URL
- 使用 SQLite 保存结果，照片 ID 重复时自动更新
- 遇到 Flickr API 错误时自动重试

## 环境要求

- Python 3.9+
- Flickr API Key 和 Secret

安装依赖：

```bash
pip install flickrapi
```

## 配置

不要把 Flickr 凭据直接写进代码或提交到 GitHub。运行前设置环境变量：

macOS / Linux：

```bash
export FLICKR_API_KEY="你的_api_key"
export FLICKR_API_SECRET="你的_api_secret"
```

Windows PowerShell：

```powershell
$env:FLICKR_API_KEY = "你的_api_key"
$env:FLICKR_API_SECRET = "你的_api_secret"
```

可选地通过 `FLICKR_DB_FILE` 指定数据库文件名；默认保存为 `flickr_yunnan3.db`。

## 使用方式

修改 `flickr_download.py` 顶部的 `KEYWORDS`、`MIN_DATE` 和 `MAX_DATE`，然后运行：

```bash
python flickr_download.py
```

脚本会在当前目录创建 SQLite 数据库。核心数据表为 `photos`，包含照片 ID、标题、图片 URL、拍摄日期、作者、经纬度、照片地点、作者地点和搜索关键词等字段。

## 注意事项

- 请遵守 Flickr API 的使用条款、速率限制和照片版权要求。
- 脚本保存的是 Flickr 返回的图片 URL 和元数据，不会自动下载图片文件。
- 照片和用户地点信息是否存在，取决于 Flickr 用户公开填写的资料。
- 大规模检索会产生较多 API 请求，运行时间可能较长。
