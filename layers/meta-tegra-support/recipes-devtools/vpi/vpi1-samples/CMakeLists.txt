option(BUILD_VIDEO_SAMPLES "Build video samples requiring ffmpeg" OFF)
set(SUBDIRS 01-convolve_2d 02-stereo_disparity 03-harris_corners 04-rescale 05-timing 07-fft 11-fisheye)
if(BUILD_VIDEO_SAMPLES)
  list(APPEND SUBDIRS 06-klt_tracker 09-tnr 10-perspwarp 12-optflow_lk)
endif()

foreach(subdir ${SUBDIRS})
  add_subdirectory(${subdir})
  string(REPLACE "-" "_" subproject ${subdir})
  install(TARGETS "vpi_sample_${subproject}" DESTINATION bin)
endforeach()

install(DIRECTORY assets/ DESTINATION assets FILE_PERMISSIONS OWNER_WRITE OWNER_READ GROUP_READ WORLD_READ)
