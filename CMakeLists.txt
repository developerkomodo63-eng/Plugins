cmake_minimum_required(VERSION 3.22)

project(DevKomodoPedals VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release CACHE STRING "Build type" FORCE)
endif()

# Keep the package lean for GitHub runners and shipping builds.
set(CMAKE_INTERPROCEDURAL_OPTIMIZATION_RELEASE ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Descarga JUCE UNA sola vez; todos los pedales de abajo la comparten.
include(FetchContent)
FetchContent_Declare(
    JUCE
    GIT_REPOSITORY https://github.com/juce-framework/JUCE.git
    GIT_TAG        8.0.15
    GIT_SHALLOW    TRUE)
FetchContent_MakeAvailable(JUCE)

# Cada pedal es un subproyecto independiente con su propio target/plugin.
add_subdirectory(Pedals/Overdrive)
add_subdirectory(Pedals/Chorus)
add_subdirectory(Pedals/Reverb)
add_subdirectory(Pedals/SynthGuitar)
add_subdirectory(Pedals/SynthBass)
add_subdirectory(Pedals/FuzzGuitar)
add_subdirectory(Pedals/DistortionGuitar)
add_subdirectory(Pedals/Compressor)
add_subdirectory(Pedals/Tremolo)
add_subdirectory(Pedals/Phaser)
add_subdirectory(Pedals/Delay)
add_subdirectory(Pedals/NoiseGate)
add_subdirectory(Pedals/Boost)
add_subdirectory(Pedals/RingModulator)
add_subdirectory(Pedals/EQ)
add_subdirectory(Pedals/EnvelopeFilterGuitar)
add_subdirectory(Pedals/OctaverGuitar)
add_subdirectory(Pedals/MultibandCompressor)
add_subdirectory(Pedals/Preamp)
add_subdirectory(Pedals/Saturator)
add_subdirectory(Pedals/VocalShifter)
add_subdirectory(Pedals/Flanger)
add_subdirectory(Pedals/AmpSim)
add_subdirectory(Pedals/Bitcrusher)
add_subdirectory(Pedals/GraphicEQ)
add_subdirectory(Pedals/Deesser)
add_subdirectory(Pedals/TransientShaper)
add_subdirectory(Pedals/Doubler)
add_subdirectory(Pedals/DrumEnhancer)
add_subdirectory(Pedals/BroadcastCompressor)
add_subdirectory(Pedals/TapeEmulation)
add_subdirectory(Pedals/VinylEmulation)
add_subdirectory(Pedals/ConvolutionReverb)
add_subdirectory(Pedals/Exciter)
add_subdirectory(Pedals/AirEnhancer)
add_subdirectory(Pedals/MonoMaker)
add_subdirectory(Pedals/PhaseAlign)
add_subdirectory(Pedals/AutoSwell)
add_subdirectory(Pedals/Vibrato)
add_subdirectory(Pedals/RotarySpeaker)
add_subdirectory(Pedals/SpringReverb)
add_subdirectory(Pedals/TapeDelay)
add_subdirectory(Pedals/GlitchMachine)
add_subdirectory(Pedals/Granulator)
add_subdirectory(Pedals/Limiter)
add_subdirectory(Pedals/Clipper)
add_subdirectory(Pedals/ConsoleEQ)
add_subdirectory(Pedals/UtilityGain)
add_subdirectory(Pedals/ToneSculptor)
add_subdirectory(Pedals/ConsoleDrive)
add_subdirectory(Pedals/CleanUpPro)

function(devkomodo_apply_compile_profile target_name)
    if(TARGET ${target_name})
        set_target_properties(${target_name} PROPERTIES
            CXX_STANDARD 17
            CXX_STANDARD_REQUIRED YES
            CXX_EXTENSIONS OFF)

        if(MSVC)
            target_compile_options(${target_name} PRIVATE
                /O2
                /Oi
                /Oy
                /GL
                /Gy
                /fp:fast)
            target_link_options(${target_name} PRIVATE
                /OPT:REF
                /OPT:ICF)
        else()
            target_compile_options(${target_name} PRIVATE
                -O3
                -DNDEBUG
                -ffast-math
                -ffunction-sections
                -fdata-sections)
            if(APPLE)
                target_link_options(${target_name} PRIVATE
                    -Wl,-dead_strip)
            else()
                target_link_options(${target_name} PRIVATE
                    -Wl,--gc-sections)
            endif()
        endif()
    endif()
endfunction()

get_property(_devkomodo_targets DIRECTORY "${CMAKE_SOURCE_DIR}" PROPERTY BUILDSYSTEM_TARGETS)
foreach(_devkomodo_target IN LISTS _devkomodo_targets)
    if(NOT _devkomodo_target MATCHES "^juce" AND TARGET ${_devkomodo_target})
        devkomodo_apply_compile_profile(${_devkomodo_target})
    endif()
endforeach()
