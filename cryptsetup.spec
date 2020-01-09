%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%if 0%{?fedora}
%if 0%{?fedora} >= 29
Obsoletes: python2-cryptsetup
Obsoletes: cryptsetup-python3
%global python2_enable 0
%global python3_enable 0
%else
%global python2_enable 1
%global python3_enable 1
%endif
%else
Obsoletes: cryptsetup-python3
%global python3_enable 0
%if 0%{?rhel} == 7
%global python2_enable 1
# Change to 1 when argon2 lands
%global libargon2_enable 0
# Change to 1 when dm-integrity gets backported
%global integritysetup_enable 0
%else
Obsoletes: cryptsetup-python
Obsoletes: python2-cryptsetup
%global python2_enable 0
%endif
%endif


Summary: A utility for setting up encrypted disks
Name: cryptsetup
Version: 2.0.3
Release: 3%{?dist}
License: GPLv2+ and LGPLv2+
Group: Applications/System
URL: https://gitlab.com/cryptsetup/cryptsetup
BuildRequires: libgcrypt-devel, popt-devel, device-mapper-devel
BuildRequires: libgpg-error-devel, libuuid-devel, libsepol-devel
BuildRequires: libselinux-devel, gcc, libblkid-devel
%if %{python2_enable}
BuildRequires: python-devel
%endif
%if %{python3_enable}
BuildRequires: python3-devel
%endif
BuildRequires: libpwquality-devel, json-c-devel
%if 0%{?libargon2_enable}
BuildRequires: libargon2-devel
%endif
Provides: cryptsetup-luks = %{version}-%{release}
Obsoletes: cryptsetup-luks < 1.4.0
Requires: cryptsetup-libs%{?_isa} = %{version}-%{release}
Requires: libpwquality >= 1.2.0

%define dracutmodulesdir %{_prefix}/lib/dracut/modules.d
%define upstream_version %{version}
%define upstream_version_old 1.7.4
Source0: https://www.kernel.org/pub/linux/utils/cryptsetup/v2.0/cryptsetup-%{upstream_version}.tar.xz
Source1: https://www.kernel.org/pub/linux/utils/cryptsetup/v1.7/cryptsetup-%{upstream_version_old}.tar.xz
# version 1.7.4 only (all of it, up to next comment)
Patch0: %{name}-avoid-rh-kernel-bug.patch
Patch1: %{name}-1.7.5-fix-unaligned-access-to-hidden-truecrypt.patch
Patch2: %{name}-1.7.5-fix-luksformat-in-fips-mode.patch
Patch3: %{name}-1.7.6-fix-blockwise-access-functions-for-64k-page-size.patch
Patch4: %{name}-1.7.6-crypt_deactivate-fail-earlier-when-holders-detected.patch
# 2.0.x only
Patch5: %{name}-2.0.4-dracut-reencrypt.patch
Patch6: %{name}-new-avoid-rh-kernel-bug.patch
Patch7: %{name}-sector-size-detection.patch
Patch8: %{name}-tests-device-test.patch
Patch9: %{name}-argon2-fips.patch
Patch10: %{name}-2.0.4-zero-length-lseek-blockwise-i-o-should-return-zero.patch
Patch11: %{name}-2.0.4-fix-write_lseek_blockwise-for-in-the-middle-of-secto.patch
Patch12: %{name}-2.0.4-fix-write_blockwise-on-short-files.patch
Patch13: %{name}-2.0.4-add-blkid-utilities-for-fast-detection-of-device-sig.patch
Patch14: %{name}-2.0.4-make-LUKS2-auto-recovery-aware-of-device-signatures.patch
Patch15: %{name}-2.0.4-allow-LUKS2-repair-to-override-blkid-checks.patch
Patch16: %{name}-2.0.4-allow-explicit-LUKS2-repair.patch
Patch17: %{name}-2.0.4-update-crypt_repair-API-documentation-for-LUKS2.patch
Patch18: %{name}-2.0.4-allow-LUKS2-repair-with-disabled-locks.patch
# the configure patch must be applied last
Patch19: %{name}-2.0.4-configure.patch
Patch20: %{name}-2.0.4-update-cryptsetup-man-page-for-type-option-usage.patch
Patch21: %{name}-2.0.4-rephrase-error-message-for-invalid-type-param-in-con.patch

%if 0%{?fedora} >= 19 || 0%{?rhel} >= 7
%define configure_cipher --enable-gcrypt-pbkdf2
%else
%define configure_cipher --with-luks1-cipher=aes --with-luks1-mode=cbc-essiv:sha256 --with-luks1-keybits=256
%endif

%if 0%{?libargon2_enable}
%define configure_libargon2 --enable-libargon2
%endif
%if 0%{?integritysetup_enable}
%define configure_integritysetup --enable-integritysetup
%else
%define configure_integritysetup --disable-integritysetup
%endif

%description
The cryptsetup package contains a utility for setting up
disk encryption using dm-crypt kernel module.

%package devel
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: libgcrypt-devel > 1.1.42, device-mapper-devel, libuuid-devel
Requires: pkgconfig
Summary: Headers and libraries for using encrypted file systems
Provides: cryptsetup-luks-devel = %{version}-%{release}
Obsoletes: cryptsetup-luks-devel < 1.4.0

%description devel
The cryptsetup-devel package contains libraries and header files
used for writing code that makes use of disk encryption.

%package libs
Group: System Environment/Libraries
Summary: Cryptsetup shared library
Provides: cryptsetup-luks-libs = %{version}-%{release}
Obsoletes: cryptsetup-luks-libs < 1.4.0
Obsoletes: cryptsetup-reencrypt-libs < 1.6.5
# Need support for empty password in gcrypt PBKDF2
%if 0%{?fedora} >= 19 || 0%{?rhel} >= 7
Requires: libgcrypt >= 1.5.3-3
%endif

%description libs
This package contains the cryptsetup shared library, libcryptsetup.

%package -n veritysetup
Group: Applications/System
Summary: A utility for setting up dm-verity volumes
Requires: cryptsetup-libs = %{version}-%{release}

%description -n veritysetup
The veritysetup package contains a utility for setting up
disk verification using dm-verity kernel module.

%package reencrypt
Group: Applications/System
Summary: A utility for offline reencryption of LUKS encrypted disks.
Provides: cryptsetup-reencrypt = %{version}-%{release}
Obsoletes: cryptsetup-reencrypt < 1.6.5
Requires: cryptsetup-libs = %{version}-%{release}

%description reencrypt
This package contains cryptsetup-reencrypt utility which
can be used for offline reencryption of disk in situ.
Also includes dracut module required to perform reencryption
of device containing a root filesystem.

%package python
Group: System Environment/Libraries
Summary: Python bindings for libcryptsetup
Requires: %{name}-libs = %{version}-%{release}
Provides: python-cryptsetup = %{version}-%{release}
Obsoletes: python-cryptsetup < 1.4.0

%description python
This package provides Python bindings for libcryptsetup, a library
for setting up disk encryption using dm-crypt kernel module.

%if %{python3_enable}
%package python3
Group: System Environment/Libraries
Summary: Python3 bindings for libcryptsetup
Requires: %{name}-libs = %{version}-%{release}
Provides: python3-cryptsetup = %{version}-%{release}

%description python3
This package provides Python bindings for libcryptsetup, a library
for setting up disk encryption using dm-crypt kernel module.
%endif

%prep
%setup -q -n cryptsetup-%{upstream_version}
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch20 -p1
%patch21 -p1
# the configure patch (always last)
%patch19 -p1
chmod -x python/pycryptsetup-test.py
chmod -x misc/dracut_90reencrypt/*

%if %{python3_enable}
# copy the whole directory for the python3 build
cp -a . %{py3dir}
%endif

%setup -T -a 1 -D -n cryptsetup-%{upstream_version}
pushd cryptsetup-1.7.4
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
%configure --enable-fips --enable-pwquality --with-default-luks-format=LUKS1 %{?configure_cipher} %{?configure_libargon2} %{?configure_integritysetup}
pushd cryptsetup-1.7.4
%configure --enable-python --enable-fips --enable-pwquality --disable-cryptsetup-reencrypt --disable-veritysetup %{?configure_cipher}
# remove rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}
popd
# remove rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}

%if %{python3_enable}
pushd %{py3dir}
%configure --enable-python --with-python_version=3
make %{?_smp_mflags}
popd
%endif

%install
pushd cryptsetup-1.7.4
make install DESTDIR=%{buildroot}
popd
make install DESTDIR=%{buildroot}
rm -rf %{buildroot}/%{_libdir}/*.la

%if %{python3_enable}
pushd %{py3dir}
make install DESTDIR=%{buildroot}
rm -rf %{buildroot}/%{_libdir}/*.la
popd
%endif

%find_lang cryptsetup

install -d -m755 %{buildroot}/%{dracutmodulesdir}/90reencrypt
install -m755 misc/dracut_90reencrypt/module-setup.sh %{buildroot}/%{dracutmodulesdir}/90reencrypt
install -m755 misc/dracut_90reencrypt/parse-reencrypt.sh %{buildroot}/%{dracutmodulesdir}/90reencrypt
install -m755 misc/dracut_90reencrypt/reencrypt.sh %{buildroot}/%{dracutmodulesdir}/90reencrypt
install -m755 misc/dracut_90reencrypt/reencrypt-verbose.sh %{buildroot}/%{dracutmodulesdir}/90reencrypt

%post -n cryptsetup-libs -p /sbin/ldconfig

%postun -n cryptsetup-libs -p /sbin/ldconfig

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc AUTHORS FAQ docs/*ReleaseNotes
%{_mandir}/man8/cryptsetup.8.gz
%{_sbindir}/cryptsetup

%files -n veritysetup
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_mandir}/man8/veritysetup.8.gz
%{_sbindir}/veritysetup

%if %{integritysetup_enable}
%files -n integritysetup
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_mandir}/man8/integritysetup.8.gz
%{_sbindir}/integritysetup
%endif

%files reencrypt
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc misc/dracut_90reencrypt/README
%{_mandir}/man8/cryptsetup-reencrypt.8.gz
%{_sbindir}/cryptsetup-reencrypt
%{dracutmodulesdir}/90reencrypt
%{dracutmodulesdir}/90reencrypt/*

%files devel
%doc docs/examples/*
%{_includedir}/libcryptsetup.h
%{_libdir}/libcryptsetup.so
%{_libdir}/pkgconfig/libcryptsetup.pc

%files libs -f cryptsetup.lang
%{!?_licensedir:%global license %%doc}
%license COPYING COPYING.LGPL
%{_libdir}/libcryptsetup.so.*
%{_tmpfilesdir}/cryptsetup.conf
%ghost %attr(700, -, -) %dir /run/cryptsetup

%files python
%{!?_licensedir:%global license %%doc}
%license COPYING.LGPL
%doc python/pycryptsetup-test.py
%exclude %{python_sitearch}/pycryptsetup.la
%{python_sitearch}/pycryptsetup.so

%if %{python3_enable}
%files python3
%{!?_licensedir:%global license %%doc}
%license COPYING.LGPL
%doc python/pycryptsetup-test.py
%exclude %{python3_sitearch}/pycryptsetup.la
%{python3_sitearch}/pycryptsetup.so
%endif

%clean

%changelog
* Tue Jul 31 2018 Ondrej Kozina <okozina@redhat.com> - 2.0.3-3
- Add expected permissions explicitly for locking directory.
- Reinstate sed script removing library rpath from libtool
  script due to bug in upstream sources distribution.
- Resolves: #1609847 #1610379

* Mon Jul 16 2018 Ondrej Kozina <okozina@redhat.com> - 2.0.3-2
- patch: stop LUKS2 auto-recovery if device is no longer LUKS
  type
- patch: update cryptsetup man page for --type option
- patch: rephrase error message for invalid --type option in
  convert action
- Resolves: #1599281 #1601477 #1601481

* Wed Jun 20 2018 Ondrej Kozina <okozina@redhat.com> - 2.0.3-1
- Update to cryptsetup 2.0.3.
- Resolves: #1475904 #1380347 #1416174 #1536105 #1574239

* Thu Oct 19 2017 Ondrej Kozina <okozina@redhat.com> - 1.7.4-4
- patch: fix regression in blockwise functions
- patch: avoid repeating error messages when device holders
  detected.
- patch: add option to cryptsetup-reencrypt to print progress
  log sequentaly
- patch: use --progress-frequency in reencryption dracut module
- Resolves: #1480006 #1447632 #1479857

* Tue Apr 25 2017 Ondrej Kozina <okozina@redhat.com> - 1.7.4-3
- patch: fix luksFormat failure while running in FIPS mode.
- Resolves: #1444137

* Tue Apr 04 2017 Ondrej Kozina <okozina@redhat.com> - 1.7.4-2
- patch: fix access to unaligned hidden TrueCrypt header.
- Resolves: #1435543

* Wed Mar 15 2017 Ondrej Kozina <okozina@redhat.com> - 1.7.4-1
- Update to cryptsetup 1.7.4.
- Resolves: #1381273

* Tue Jun  7 2016 Ondrej Kozina <okozina@redhat.com> - 1.7.2-1
- Update to cryptsetup 1.7.2.
- Resolves: #1302022 #1070825

* Thu Jun 18 2015 Ondrej Kozina <okozina@redhat.com> - 1.6.7-1
- Update to cryptsetup 1.6.7.
- patch: avoid use of kernel crypto API socket which is known
  to be broken in RHEL7.0 kernel (7.1+ is fine).
- Resolves: #1206170

* Thu Dec 18 2014 Ondrej Kozina <okozina@redhat.com> - 1.6.6-3
- drop FIPS power on self test and library checksum
- Resolves: #1158897

* Mon Sep 29 2014 Ondrej Kozina <okozina@redhat.com> - 1.6.6-2
- patch: fix failures related to reencrypt log files
- Resolves: #1140199

* Mon Sep  8 2014 Ondrej Kozina <okozina@redhat.com> - 1.6.6-1
- Update to cryptsetup 1.6.6.
- Resolves: #1117372 #1038097

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1.6.3-2
- Mass rebuild 2014-01-24

* Mon Jan 6 2014 Ondrej Kozina <okozina@redhat.com> - 1.6.3-1
- Update to cryptsetup 1.6.3.
- various fixes related to block devices with 4KiB sectors
- enable reencryption using specific keyslot (dracut module)
- fix failure in reading last keyslot from external LUKS header
- update FIPS POST to be complaint with actual requirements
- fix hash limiting if parameter is not numeric
- Resolves: #1028362 #1029032 #1029406 #1030288 #1034388 #1038097

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.6.2-3
- Mass rebuild 2013-12-27

* Tue Nov 5 2013 Ondrej Kozina <okozina@redhat.com> - 1.6.2-2
- 90reencrypt: Move conflict with 90crypt to install() section.
- 90reencrypt: Drop to emergency_shell after successful reencryption.
- Resolves: #1021593

* Mon Oct 14 2013 Ondrej Kozina <okozina@redhat.com> - 1.6.2-1
- Update to cryptsetup 1.6.2.
- Add dracut module for cryptsetup-reencrypt (90reencrypt).
- 90reencrypt: Rename dracut parameteres to be compliant with actual naming guidance.
- 90reencrypt: Install and load loop kernel module.
- 90reencrypt: Fix lock file name.
- 90reencrypt: Add conflict with 90crypt dracut module (more info in #1010287)
- Resolves: #1010278 #1010287

* Sun Mar 31 2013 Milan Broz <gmazyland@gmail.com> - 1.6.1-1
- Update to cryptsetup 1.6.1.
- Install ReleaseNotes files instead of empty Changelog file.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 14 2013 Milan Broz <mbroz@redhat.com> - 1.6.0-1
- Update to cryptsetup 1.6.0.
- Change default LUKS encryption mode to aes-xts-plain64 (AES128).
- Force use of gcrypt PBKDF2 instead of internal implementation.

* Sat Dec 29 2012 Milan Broz <mbroz@redhat.com> - 1.6.0-0.1
- Update to cryptsetup 1.6.0-rc1.
- Relax license to GPLv2+ according to new release.
- Compile cryptsetup with libpwquality support.

* Tue Oct 16 2012 Milan Broz <mbroz@redhat.com> - 1.5.1-1
- Update to cryptsetup 1.5.1.

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Milan Broz <mbroz@redhat.com> - 1.5.0-1
- Update to cryptsetup 1.5.0.

* Wed Jun 20 2012 Milan Broz <mbroz@redhat.com> - 1.5.0-0.2
- Update to cryptsetup 1.5.0-rc2.
- Add cryptsetup-reencrypt subpackage.

* Mon Jun 11 2012 Milan Broz <mbroz@redhat.com> - 1.5.0-0.1
- Update to cryptsetup 1.5.0-rc1.
- Add veritysetup subpackage.
- Move localization files to libs subpackage.

* Thu May 31 2012 Milan Broz <mbroz@redhat.com> - 1.4.3-2
- Build with fipscheck (verification in fips mode).
- Clean up spec file, use install to /usr.

* Thu May 31 2012 Milan Broz <mbroz@redhat.com> - 1.4.3-1
- Update to cryptsetup 1.4.3.

* Thu Apr 12 2012 Milan Broz <mbroz@redhat.com> - 1.4.2-1
- Update to cryptsetup 1.4.2.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 09 2011 Milan Broz <mbroz@redhat.com> - 1.4.1-1
- Update to cryptsetup 1.4.1.
- Add Python cryptsetup bindings.
- Obsolete separate python-cryptsetup package.

* Wed Oct 26 2011 Milan Broz <mbroz@redhat.com> - 1.4.0-1
- Update to cryptsetup 1.4.0.

* Mon Oct 10 2011 Milan Broz <mbroz@redhat.com> - 1.4.0-0.1
- Update to cryptsetup 1.4.0-rc1.
- Rename package back from cryptsetup-luks to cryptsetup.

* Wed Jun 22 2011 Milan Broz <mbroz@redhat.com> - 1.3.1-2
- Fix return code for status command when device doesn't exist.

* Tue May 24 2011 Milan Broz <mbroz@redhat.com> - 1.3.1-1
- Update to cryptsetup 1.3.1.

* Tue Apr 05 2011 Milan Broz <mbroz@redhat.com> - 1.3.0-1
- Update to cryptsetup 1.3.0.

* Tue Mar 22 2011 Milan Broz <mbroz@redhat.com> - 1.3.0-0.2
- Update to cryptsetup 1.3.0-rc2

* Mon Mar 14 2011 Milan Broz <mbroz@redhat.com> - 1.3.0-0.1
- Update to cryptsetup 1.3.0-rc1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Milan Broz <mbroz@redhat.com> - 1.2.0-1
- Update to cryptsetup 1.2.0

* Thu Nov 25 2010 Milan Broz <mbroz@redhat.com> - 1.2.0-0.2
- Fix crypt_activate_by_keyfile() to work with PLAIN devices.

* Tue Nov 16 2010 Milan Broz <mbroz@redhat.com> - 1.2.0-0.1
- Add FAQ to documentation.
- Update to cryptsetup 1.2.0-rc1

* Sat Jul 03 2010 Milan Broz <mbroz@redhat.com> - 1.1.3-1
- Update to cryptsetup 1.1.3

* Mon Jun 07 2010 Milan Broz <mbroz@redhat.com> - 1.1.2-2
- Fix alignment ioctl use.
- Fix API activation calls to handle NULL device name.

* Sun May 30 2010 Milan Broz <mbroz@redhat.com> - 1.1.2-1
- Update to cryptsetup 1.1.2
- Fix luksOpen handling of new line char on stdin.

* Sun May 23 2010 Milan Broz <mbroz@redhat.com> - 1.1.1-1
- Update to cryptsetup 1.1.1
- Fix luksClose for stacked LUKS/LVM devices.

* Mon May 03 2010 Milan Broz <mbroz@redhat.com> - 1.1.1-0.2
- Update to cryptsetup 1.1.1-rc2.

* Sat May 01 2010 Milan Broz <mbroz@redhat.com> - 1.1.1-0.1
- Update to cryptsetup 1.1.1-rc1.

* Sun Jan 17 2010 Milan Broz <mbroz@redhat.com> - 1.1.0-1
- Update to cryptsetup 1.1.0.

* Fri Jan 15 2010 Milan Broz <mbroz@redhat.com> - 1.1.0-0.6
- Fix gcrypt initialisation.
- Fix backward compatibility for hash algorithm (uppercase).

* Wed Dec 30 2009 Milan Broz <mbroz@redhat.com> - 1.1.0-0.5
- Update to cryptsetup 1.1.0-rc4

* Mon Nov 16 2009 Milan Broz <mbroz@redhat.com> - 1.1.0-0.4
- Update to cryptsetup 1.1.0-rc3

* Thu Oct 01 2009 Milan Broz <mbroz@redhat.com> - 1.1.0-0.3
- Update to cryptsetup 1.1.0-rc2
- Fix libcryptsetup to properly export only versioned symbols.

* Tue Sep 29 2009 Milan Broz <mbroz@redhat.com> - 1.1.0-0.2
- Update to cryptsetup 1.1.0-rc1
- Add luksHeaderBackup and luksHeaderRestore commands.

* Fri Sep 11 2009 Milan Broz <mbroz@redhat.com> - 1.1.0-0.1
- Update to new upstream testing version with new API interface.
- Add luksSuspend and luksResume commands.
- Introduce pkgconfig.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 Milan Broz <mbroz@redhat.com> - 1.0.7-1
- Update to upstream final release.
- Split libs subpackage.
- Remove rpath setting from cryptsetup binary.

* Wed Jul 15 2009 Till Maas <opensource@till.name> - 1.0.7-0.2
- update BR because of libuuid splitout from e2fsprogs

* Mon Jun 22 2009 Milan Broz <mbroz@redhat.com> - 1.0.7-0.1
- Update to new upstream 1.0.7-rc1.

- Wipe old fs headers to not confuse blkid (#468062)
* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Oct 30 2008 Milan Broz <mbroz@redhat.com> - 1.0.6-6
- Wipe old fs headers to not confuse blkid (#468062)

* Tue Sep 23 2008 Milan Broz <mbroz@redhat.com> - 1.0.6-5
- Change new project home page.
- Print more descriptive messages for initialization errors.
- Refresh patches to versions commited upstream.

* Sat Sep 06 2008 Milan Broz <mbroz@redhat.com> - 1.0.6-4
- Fix close of zero decriptor.
- Fix udevsettle delays - use temporary crypt device remapping.

* Wed May 28 2008 Till Maas <opensource till name> - 1.0.6-3
- remove a duplicate sentence from the manpage (RH #448705)
- add patch metadata about upstream status

* Tue Apr 15 2008 Bill Nottinghm <notting@redhat.com> - 1.0.6-2
- Add the device to the luksOpen prompt (#433406)
- Use iconv, not recode (#442574)

* Thu Mar 13 2008 Till Maas <opensource till name> - 1.0.6-1
- Update to latest version
- remove patches that have been merged upstream

* Mon Mar 03 2008 Till Maas <opensource till name> - 1.0.6-0.1.pre2
- Update to new version with several bugfixes
- remove patches that have been merged upstream
- add patch from cryptsetup newsgroup
- fix typo / missing luksRemoveKey in manpage (patch)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.5-9
- Autorebuild for GCC 4.3

* Sat Jan 19 2008 Peter Jones <pjones@redhat.com> - 1.0.5-8
- Rebuild for broken deps.

* Thu Aug 30 2007 Till Maas <opensource till name> - 1.0.5-7
- update URL
- update license tag
- recode ChangeLog from latin1 to uf8
- add smp_mflags to make

* Fri Aug 24 2007 Till Maas <opensource till name> - 1.0.5-6
- cleanup BuildRequires:
- removed versions, packages in Fedora are new enough
- changed popt to popt-devel

* Thu Aug 23 2007 Till Maas <opensource till name> - 1.0.5-5
- fix devel subpackage requires
- remove empty NEWS README
- remove uneeded INSTALL
- remove uneeded ldconfig requires
- add readonly detection patch

* Wed Aug 08 2007 Till Maas <opensource till name> - 1.0.5-4
- disable patch2, libsepol is now detected by configure
- move libcryptsetup.so to %%{_libdir} instead of /%%{_lib}

* Fri Jul 27 2007 Till Maas <opensource till name> - 1.0.5-3
- Use /%%{_lib} instead of /lib to use /lib64 on 64bit archs

* Thu Jul 26 2007 Till Maas <opensource till name> - 1.0.5-2
- Use /lib as libdir (#243228)
- sync header and library (#215349)
- do not use %%makeinstall (recommended by PackageGuidelines)
- select sbindir with %%configure instead with make
- add TODO

* Wed Jun 13 2007 Jeremy Katz <katzj@redhat.com> - 1.0.5-1
- update to 1.0.5

* Mon Jun 04 2007 Peter Jones <pjones@redhat.com> - 1.0.3-5
- Don't build static any more.

* Mon Feb 05 2007 Alasdair Kergon <agk@redhat.com> - 1.0.3-4
- Add build dependency on new device-mapper-devel package.
- Add preun and post ldconfig requirements.
- Update BuildRoot.

* Wed Nov  1 2006 Peter Jones <pjones@redhat.com> - 1.0.3-3
- Require newer libselinux (#213414)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.0.3-2.1
- rebuild

* Wed Jun  7 2006 Jeremy Katz <katzj@redhat.com> - 1.0.3-2
- put shared libs in the right subpackages

* Fri Apr  7 2006 Bill Nottingham <notting@redhat.com> 1.0.3-1
- update to final 1.0.3

* Mon Feb 27 2006 Bill Nottingham <notting@redhat.com> 1.0.3-0.rc2
- update to 1.0.3rc2, fixes bug with HAL & encrypted devices (#182658)

* Wed Feb 22 2006 Bill Nottingham <notting@redhat.com> 1.0.3-0.rc1
- update to 1.0.3rc1, reverts changes to default encryption type

* Tue Feb 21 2006 Bill Nottingham <notting@redhat.com> 1.0.2-1
- update to 1.0.2, fix incompatiblity with old cryptsetup (#176726)

* Mon Feb 20 2006 Karsten Hopp <karsten@redhat.de> 1.0.1-5
- BuildRequires: libselinux-devel

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.0.1-4.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.0.1-4.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Dec  5 2005 Bill Nottingham <notting@redhat.com> 1.0.1-4
- rebuild against new libdevmapper

* Thu Oct 13 2005 Florian La Roche <laroche@redhat.com>
- add -lsepol to rebuild on current fc5

* Mon Aug 22 2005 Karel Zak <kzak@redhat.com> 1.0.1-2
- fix cryptsetup help for isLuks action

* Fri Jul  1 2005 Bill Nottingham <notting@redhat.com> 1.0.1-1
- update to 1.0.1 - fixes incompatiblity with previous cryptsetup for
  piped passwords

* Thu Jun 16 2005 Bill Nottingham <notting@redhat.com> 1.0-2
- add patch for 32/64 bit compatibility (#160445, <redhat@paukstadt.de>)

* Tue Mar 29 2005 Bill Nottingham <notting@redhat.com> 1.0-1
- update to 1.0

* Thu Mar 10 2005 Bill Nottingham <notting@redhat.com> 0.993-1
- switch to cryptsetup-luks, for LUKS support

* Tue Oct 12 2004 Bill Nottingham <notting@redhat.com> 0.1-4
- oops, make that *everything* static (#129926)

* Tue Aug 31 2004 Bill Nottingham <notting@redhat.com> 0.1-3
- link some things static, move to /sbin (#129926)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Apr 16 2004 Bill Nottingham <notting@redhat.com> 0.1-1
- initial packaging
