<h1 align="center">📺bilibili-to-evernote🐘</h1>
<p align="center">
  <img src="https://img.shields.io/badge/version-0.1.0-blue.svg?cacheSeconds=2592000" />
  <a href="https://twitter.com/Miracle_XYZ">
    <img alt="Twitter: Miracle_XYZ" src="https://img.shields.io/twitter/follow/Miracle_XYZ.svg?style=social" target="_blank" />
  </a>
</p>

> 一个将B站动态保存到Evernote（印象笔记）的工具

## 安装

### 子模块初始化

首先安装 submodule `evernote`:

``` sh
git clone git@github.com:MiracleXYZ/bilibili-to-evernote.git
git submodule init
git submodule update
```

或者直接

``` sh
git clone --recursive git@github.com:MiracleXYZ/bilibili-to-evernote.git
```

### 安装 `evernote` 库

``` sh
cd evernote
python setup.py install
```

### 安装依赖

#### 通过requirements

``` sh
pip install -r requirements.txt
```

#### 通过poetry

``` sh
poetry install
```

## 使用

### 创建配置文件 `config.toml`

`config.toml.example` 是一个配置文件的示例。实际使用时，将其更名或复制为 `config.toml` 即可。

### 申请API Token

到网站 https://app.yinxiang.com/api/DeveloperToken.action 申请API Token，并将 `config.toml` 中 `[client]` 部分的 `token` 属性改为你申请到的Token。

> 请像保存**你的印象笔记密码**一样保存这个token！只要有人拿到这个token，理论上他能对你的账号做任何事情……

### 保存笔记

```sh
python main.py h [doc-id]
python main.py t [dynamic-id]
```

目前支持：

- 哔哩哔哩相簿
  - 网址：`https://h.bilibili.com/{doc_id}`
  - 命令：`python main.py h {doc_id}`
- 图片动态（或转发图片动态的动态）
  - 网址：`https://t.bilibili.com/{dynamic_id}`
  - 命令：`python main.py t {dynamic_id}`
- 其他还在完善中，如有需求欢迎 [提issue](https://github.com/MiracleXYZ/bilibili-to-evernote/issues) 。

## 作者

👤 **MiracleXYZ**

* Twitter: [@Miracle_XYZ](https://twitter.com/Miracle_XYZ)
* Github: [@MiracleXYZ](https://github.com/MiracleXYZ)

## 🤝 贡献

欢迎提issue、请求功能、开PR！

有问题或建议的话到 [issues page](https://github.com/MiracleXYZ/bilibili-to-evernote/issues) ，都可以提，都提

## Show your support

觉得好就赏个⭐️吧~

***
_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_