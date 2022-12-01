package com.example.livestreamdemo.video

import android.content.Context
import androidx.lifecycle.LifecycleEventObserver
import androidx.lifecycle.LifecycleOwner

class VideoCaptureManager private constructor(private val builder: Builder) : LifecycleEventObserver {

    init {
        getLifecycle().addObserver(this)
    }



    class Builder(val context: Context) {

        var lifecycleOwner: LifecycleOwner? = null
            private set

        fun registerLifecycleOwner(source: LifecycleOwner): Builder {
            this.lifecycleOwner = source
            return this
        }

        fun create(): VideoCaptureManager {
            requireNotNull(lifecycleOwner) { "Lifecycle owner is not set" }
            return VideoCaptureManager(this)
        }
    }
}