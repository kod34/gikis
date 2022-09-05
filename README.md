<h1 align="center"><b>gikis</b></h1>

<p align="center"> A web crawler that takes into input a URL, a level of digging and an output directory which will contain the web pages to be downloaded for the purpose of being opened locally without the need for internet access.
    <br> 
</p>

## 📝 Table of Contents

- [Installing](#Installing)
- [Usage](#usage)
- [Authors](#authors)


## Installing


```
git clone https://github.com/kod34/gikis

cd gikis/

pip3 install -r requirements.txt
```


## 🎈 Usage <a name="usage"></a>
```
usage: gikis.py [-h] -u URL -o OUT -l LVL [-d DELAY]

options:
  -h, --help  show this help message and exit

required named arguments:
  -u URL      Specify a url
  -o OUT      Specify an output directory
  -l LVL      Specify a level (basic, light, moderate, deep)
  -d DELAY    Specify a download delay
```
Example:

`gikis.py -u http://docs.example.com -l light -o directory/ -d 5
`

## ✍️ Authors <a name = "authors"></a>

- [@danielo37](https://github.com/danielo37) - Idea
- [@kod34](https://github.com/kod34) - Coding

