#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''

import threading
mutex = threading.Lock()

class Singleton(object):
    def __new__(cls,*args,**kwags):
        # 关键在于这，每一次实例化的时候，我们都只会返回这同一个instance对象
        # 同时做双重检查，在多线程情况下，如果两个线程同时到达，
        # 则第一个条件not hasattr(cls, 'instance')都满足，这时由于有线程锁锁住，
        # 则有一个线程会继续走下去而另外一个线程会被锁住
        # 第一个线程执行完后，被锁住的线程会开始执行下去。
        # 而这时如果没有第二个判断的话，刚才退出锁定的线程会新创建一个实例。这样就不是单例了。
        # 故必须要做双重判断。而第一个判断则可以提高性能。也就是多线程的时候只有当没有instance这个静态变量的
        # 时候再会触发锁。而如果没有那么每一次都会触发锁。这样会带来的性能问题。
        if not hasattr(cls, 'instance'):
            try:
                mutex.acquire()
                if not hasattr(cls, 'instance'):
                    cls.instance = super(Singleton, cls).__new__(cls,*args,**kwags)
            finally:
                mutex.release()
        return cls.instance
    
    
    
obj1 = Singleton()
obj2 = Singleton()
obj1.attr1 = 'value1'
print obj1.attr1, obj2.attr1
print obj1 is obj2
print id(obj1)
print id(obj2)
'''



import threading
import time
#这里使用方法__new__来实现单例模式

#修改
mutex = threading.Lock()

class Singleton(object):#抽象单例
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            try:
                mutex.acquire()
                if not hasattr(cls, 'instance'):
                    orig = super(Singleton, cls)
                    cls._instance = orig.__new__(cls, *args, **kw)
            finally:
                mutex.release()
        return cls._instance
#总线
class Bus(Singleton):
    lock = threading.RLock()
    def sendData(self,data):
        self.lock.acquire()
        time.sleep(3)
        print "Sending Signal Data...",data
        self.lock.release()
#线程对象，为更加说明单例的含义，这里将Bus对象实例化写在了run里
class VisitEntity(threading.Thread):
    my_bus=""
    name=""
    def getName(self):
        return self.name
    def setName(self, name):
        self.name=name
    def run(self):
        self.my_bus=Bus()
        self.my_bus.sendData(self.name)

if  __name__=="__main__":
    for i in range(3):
        print "Entity %d begin to run..."%i
        my_entity=VisitEntity()
        my_entity.setName("Entity_"+str(i))
        my_entity.start()