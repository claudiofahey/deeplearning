
# damianmoore/tensorflow-image-classifier

Start TensorBoard:
```
docker-compose up -d
```
Then point your browser to:
<http://localhost:6006/>

Training:
```
faheyc@ubuntu:~/deeplearning/tensorflow-image-classifier$
./train.sh ../data/tf_files flowers -s 4000
faheyc@ubuntu:~/deeplearning/tensorflow-image-classifier$
./classify.sh ../data/tf_files flowers ../data/tf_files/flowers/data/daisy/11124324295_503f3a0804.jpg
```

```
sudo apt-get install imagemagick
```

# References

- <https://github.com/damianmoore/tensorflow-image-classifier>
