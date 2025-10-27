AC_PREREQ(2.52)

AC_INIT([Apertium Ido-Esperanto], [0.1.0], [mark@example.com], [apertium-ido-epo], [https://wiki.apertium.org/wiki/Apertium-ido-epo])
AM_INIT_AUTOMAKE([-Wall -Werror foreign])

AC_PROG_LN_S
AC_PROG_AWK

m4_define([required_apertium_version], [3.4.0])
m4_define([required_lttoolbox_version], [3.3.2])

PKG_CHECK_MODULES(APERTIUM, apertium >= required_apertium_version)
PKG_CHECK_MODULES(LTTOOLBOX, lttoolbox >= required_lttoolbox_version)

AC_PATH_PROG([CGCOMP], [cg-comp], [false], [$PATH$PATH_SEPARATOR$with_cg_comp/bin])
AS_IF([test x$CGCOMP = xfalse], [AC_MSG_ERROR([You don't have cg-comp installed])])

PKG_CHECK_MODULES(REGTEST, apertium-regtest >= 0.0.1, [],
                  [AC_MSG_WARN([Running tests requires apertium-regtest])])

# Find source directories for monolingual dictionaries
AP_SRC1=`pkg-config --variable=dir apertium-ido 2>/dev/null || echo "/usr/local/share/apertium/apertium-ido"`
AP_SRC2=`pkg-config --variable=dir apertium-epo 2>/dev/null || echo "/usr/share/apertium/apertium-epo"`
AC_SUBST(AP_SRC1)
AC_SUBST(AP_SRC2)

AP_MKINCLUDE

AC_OUTPUT([Makefile apertium-ido-epo.pc])
