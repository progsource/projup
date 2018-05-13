macro(change_include_dir oldDir newDir)
  file(GLOB_RECURSE includeFiles RELATIVE ${oldDir} ${oldDir}/*)
  foreach(includeFile ${includeFiles})
    configure_file(
      ${oldDir}/${includeFile}
      ${newDir}/${includeFile}
      COPYONLY
    )
  endforeach()
  message(STATUS "changed includeDir from ${White}${oldDir}${Green} to ${White}${newDir}${Green}")
endmacro(change_include_dir)
