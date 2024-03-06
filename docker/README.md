# mysite development using Docker Compose

> Note that this is for **development only**, the containers spawned for
this project are configured for development ease, not security.

Also see <https://docs.docker.com/compose/overview/>

The setup provides these containers:

* nginx
* python (custom image)
* postgres
* node (custom image)

## To run locally:

### 0. Make sure Docker Desktop and mkcert are installed

#### Docker Desktop

<https://docs.docker.com/docker-for-mac/install/> or `brew cask install docker`

#### mkcert

<https://github.com/FiloSottile/mkcert>

```sh
brew install mkcert
brew install nss  # if you use Firefox
mkcert -install
```

### 1. Create certificates to access the site via https

Create a local (wildcard) cert using `mkcert`

```sh
mkcert -cert-file ./docker/conf/certs/cert.pem -key-file \
       ./docker/conf/certs/key.pem \
       mysite.test "*.mysite.test"
```

Also copy the mkcert root CA cert to the `conf/certs` directory:

```sh
cp "$(mkcert -CAROOT)/rootCA.pem" ./docker/conf/certs/ca.pem
```

### 2. Configure `/etc/hosts/`

Add the following lines to `/etc/hosts`:

```
127.0.0.1       mysite.test www.mysite.test
127.0.0.1       histoire.mysite.test
```

> *TIP*: [Gas Mask](https://github.com/2ndalpha/gasmask) is a nice tool
to manage host file entries. Install with `brew cask install gas-mask`


### 3. Configure project settings (optional)

On startup, the `python` container will copy `mysite/local.example.ini` to
`mysite/local.ini` (if it does not yet exist).

To manually configure the settings, first copy the example file:

```sh
cp content/local.example.ini content/local.ini
```

Then edit the settings to your liking.


### 4. Running the containers

Normally, you start all containers in the foreground:

```sh
docker-compose up
```

You can also start all containers in the background:

```sh
docker-compose up -d
```


### 5. First run?

With the `python` container running execute these commands:

```sh
docker-compose exec python ./content/manage.py createsuperuser
```

> Note: This list of commands may be incomplete, make sure to also look
at the `README` files of this project for more instructions.


### 6. Visit the pages

- Wagtail App <https://www.mysite.test/>
- Wagtail Admin <https://www.mysite.test/wagtail-admin/>
- Nuxt App <http://www.mysite.test/{anything}>

### 7. Extra Wagtail config

Follow the instructions on [README.md](../README.md).
