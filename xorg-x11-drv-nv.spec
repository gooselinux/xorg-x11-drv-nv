%define tarball xf86-video-nv
%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define driverdir	%{moduledir}/drivers

Summary:   Xorg X11 nv video driver
Name:      xorg-x11-drv-nv
Version:   2.1.15
Release:   4%{?dist}
URL:       http://www.x.org
License: MIT
Group:     User Interface/X Hardware Support
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:   ftp://ftp.x.org/pub/individual/driver/%{tarball}-%{version}.tar.bz2
Source1:   nv.xinf

ExcludeArch: s390 s390x

BuildRequires: xorg-x11-server-devel >= 1.6.0
BuildRequires: libdrm-devel >= 2.3.0-7

Requires:  hwdata
Requires:  xorg-x11-server-Xorg >= 1.6.0

Patch4:     nv-reserve-fbarea.patch
Patch5:	    nv-2.1.6-starvation.patch
Patch6:	    nv-2.1.6-panel-fix.patch
Patch7:	    nv-save-rom.patch
Patch9:	    nv-2.1.8-g80-no-doublescan.patch
Patch10:    nv-2.1.12-gf7025-gf7050.patch
Patch11:    nv-refuse-kms.patch
Patch12:    nv-2.1.15-g80-nop-gamma.patch
Patch13:    nv-2.1.15-g80-update.patch

%description 
X.Org X11 nv video driver.

%prep
%setup -q -n %{tarball}-%{version}

%patch4 -p1 -b .reserve-fbarea
%patch5 -p1 -b .starve
%patch6 -p1 -b .panel
%patch7 -p1 -b .save-rom
%patch9 -p1 -b .doublescan
%patch10 -p1 -b .nv6x
%patch11 -p1 -b .nokms
%patch12 -p1 -b .gamma
%patch13 -p1 -b .g80-update

%build
autoreconf -v --install
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_datadir}/hwdata/videoaliases
install -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/hwdata/videoaliases/

find $RPM_BUILD_ROOT -regex ".*\.la$" | xargs rm -f --

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc COPYING README.G80
%{driverdir}/nv_drv.so
%{_datadir}/hwdata/videoaliases/nv.xinf
%{_mandir}/man4/nv.4*

%changelog
* Thu Nov 12 2009 Adam Jackson <ajax@redhat.com> 2.1.15-4
- nv.xinf: Update for same.

* Thu Nov 12 2009 Adam Jackson <ajax@redhat.com> 2.1.15-3
- nv-2.1.15-g80-update.patch: Add new G80 ASIC support.

* Wed Oct 28 2009 Adam Jackson <ajax@redhat.com> 2.1.15-2
- nv-2.1.15-g80-nop-gamma.patch: Install a no-op gamma hook so we don't
  crash immediately on init.

* Fri Sep 11 2009 Ben Skeggs <bskeggs@redhat.com> 2.1.15-1
- nv 2.1.15

* Fri Aug 28 2009 Ben Skeggs <bskeggs@redhat.com> 2.1.14-5
- refuse to load if KMS driver already using the hw

* Tue Aug 04 2009 Adam Jackson <ajax@redhat.com> 2.1.14-4
- autoreconf so the dpms configurey gets picked up

* Tue Aug 04 2009 Dave Airlie <airlied@redhat.com> 2.1.14-3
- update for new ABI

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.14-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Adam Jackson <ajax@redhat.com> - 2.1.14-1.1
- ABI bump

* Tue Jul 07 2009 Adam Jackson <ajax@redhat.com> 2.1.14-1
- nv 2.1.14

* Tue Jun 23 2009 Dave Airlie <airlied@redhat.com> 2.1.13-2
- patch for new server ABI

* Tue Apr 07 2009 Adam Jackson <ajax@redhat.com> 2.1.13-1
- nv 2.1.13
- nv.xinf: Add 7025/7050.

* Fri Feb 27 2009 Adam Jackson <ajax@redhat.com> 2.1.12-11
- nv-2.1.12-eedid.patch: Do E-EDID.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.12-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb 21 2009 Adam Jackson <ajax@redhat.com> 2.1.12-9
- Merge review cleanups (#226612)

* Tue Feb 17 2009 Ben Skeggs <bskeggs@redhat.com> 2.1.12-8
- Add support for GeForce 7025/7050 (fdo #22371)

* Mon Dec 22 2008 Dave Airlie <airlied@redhat.com> 2.1.12-7
- rebuild for new server API

* Wed Oct 22 2008 Adam Jackson <ajax@redhat.com> 2.1.12-6
- nv-2.1.8-g80-no-doublescan.patch: Disable doublescan on G80, too many
  monitors get confused.

* Tue Sep 30 2008 Dan Williams <dcbw@redhat.com> 2.1.12-5
- Port Toshiba Tecra M2 NV34 panel tweak to pciaccess

* Thu Sep 11 2008 Soren Sandmann <sandmann@redhat.com> 2.1.12-4
- Remove fb size hack since there is a fix in the server now.

* Wed Sep 10 2008 Adam Jackson <ajax@redhat.com> 2.1.12-3
- Do the fb size hack a differently wretched way.

* Mon Sep 08 2008 Adam Jackson <ajax@redhat.com> 2.1.12-2
- nv-2.1.12-fb-size.patch: Yet more lame heuristics to preallocate a usable
  framebuffer for laptops. (#458864)

* Thu Aug 28 2008 Adam Jackson <ajax@redhat.com> 2.1.12-1
- nv 2.1.12

* Wed Aug 27 2008 Adam Jackson <ajax@redhat.com> 2.1.11-1
- nv 2.1.11

* Fri Aug 01 2008 Adam Jackson <ajax@redhat.com> 2.1.10-1
- nv 2.1.10

* Tue May 20 2008 Matthew Garrett <mjg@redhat.com> 2.1.8-2
- nv-save-rom.patch: save the rom at startup on g80s to allow them to be 
  rePOSTed on resume.

* Fri Mar 07 2008 Adam Jackson <ajax@redhat.com> 2.1.8-1
- nv 2.1.8

* Mon Mar 03 2008 Dave Airlie <airlied@redhat.com> 2.1.7-3
- update for new server ABI

* Fri Feb 29 2008 Dave Airlie <airlied@redhat.com> 2.1.7-2
- drop nouveau sub-package

* Fri Feb 22 2008 Adam Jackson <ajax@redhat.com> 2.1.7-1
- nv 2.1.7

* Tue Feb 12 2008 Adam Jackson <ajax@redhat.com> 2.1.6-8
- nv-2.1.6-panel-fix.patch: Don't discard EDID blocks just because their
  input type bit disagrees with the hardware connection sensing; this
  usually just means the block is lying. (#294861)

* Wed Jan 23 2008 Adam Jackson <ajax@redhat.com> 2.1.6-7
- nv-2.1.6-starvation.patch: Typo fix.

* Tue Jan 22 2008 Adam Jackson <ajax@redhat.com> 2.1.6-6
- nv-2.1.6-starvation.patch: Avoid starving nv4-gen chips of memory
  bandwidth on huge modes.  There's surely a better way to do this.
  (#383891)

* Fri Jan 18 2008 Dave Airlie <airlied@redhat.com> 2.1.6-5
- fixup the fixup for fb vs XAA alignment

* Fri Jan 18 2008 Dave Airlie <airlied@redhat.com> 2.1.6-4
- Fixup fb vs XAA alignment

* Wed Jan 09 2008 Adam Jackson <ajax@redhat.com> 2.1.6-3
- Rebuild yet again for new server ABI.

* Tue Nov 13 2007 Adam Jackson <ajax@redhat.com> 2.1.6-2
- Require new server ABI.

* Mon Nov 12 2007 Adam Jackson <ajax@redhat.com> 2.1.6-1
- xf86-video-nv 2.1.6

* Thu Oct 11 2007 Dave Airlie <airlied@redhat.com> 2.1.5-2
- nouveau-fix-bswap32.patch - fix nouveau driver on ppc/ppc64

* Mon Sep 24 2007 Adam Jackson <ajax@redhat.com> 2.1.5-1
- xf86-video-nv 2.1.5.

* Thu Sep 20 2007 Dave Airlie <airlied@redhat.com> 2.1.3-2
- update nouveau

* Fri Aug 17 2007 Adam Jackson <ajax@redhat.com> 2.1.3-1
- xf86-video-nv 2.1.3.

* Tue Jul 10 2007 Adam Jackson <ajax@redhat.com> 2.1.2-1
- xf86-video-nv 2.1.2.

* Tue Jul 03 2007 Adam Jackson <ajax@redhat.com> 2.1.1-1
- xf86-video-nv 2.1.1.

* Tue Jun 26 2007 Adam Jackson <ajax@redhat.com> 2.1.0-2
- %%doc for COPYING and README.G80.

* Tue Jun 19 2007 Adam Jackson <ajax@redhat.com> 2.1.0-1
- xf86-video-nv 2.1.0.

* Mon Jun 18 2007 Adam Jackson <ajax@redhat.com> 2.0.96-4
- Update Requires and BuildRequires.  Add Requires: hwdata.

* Wed Jun 06 2007 Adam Jackson <ajax@redhat.com> 2.0.96-3
- Backport of G80 LVDS (laptop) support from git master.

* Mon Jun 04 2007 Adam Jackson <ajax@redhat.com> 2.0.96-2
- Meaningless version bump.

* Fri May 18 2007 Adam Jackson <ajax@redhat.com> 2.0.96-1
- nv 2.0.96.  Add rudimentary dual-head support for pre-G80 cards.

* Fri May 11 2007 Adam Jackson <ajax@redhat.com> 2.0.95-1
- nv 2.0.95.  Adds RandR 1.2 and EXA support for G80 series.

* Thu May 03 2007 Adam Jackson <ajax@redhat.com> 2.0.2-2
- Split nouveau into its own binary package.

* Tue Apr 17 2007 Adam Jackson <ajax@redhat.com> 2.0.2-1
- nv 2.0.2
- nv.xinf: PCI ID updates for yet more G80 cards.
- Drop panel-range-hack, superceded upstream now.

* Mon Apr  2 2007 Kristian Høgsberg <krh@redhat.com> - 2.0.1-3
- Add nv patches to nouveau too.

* Fri Mar 30 2007 Kristian Høgsberg <krh@redhat.com> 2.0.1-2
- Update nouveau snapshot.

* Fri Mar 30 2007 Adam Jackson <ajax@redhat.com> 2.0.1-1
- nv 2.0.1

* Fri Mar 23 2007 Adam Jackson <ajax@redhat.com> 2.0.0-3
- nv.xinf: It helps if you spell the driver name correctly.

* Tue Mar 20 2007 Adam Jackson <ajax@redhat.com> 2.0.0-2
- nv-2.0.0-hang-fix.patch: Fix a hang during initialization.

* Mon Mar 19 2007 Adam Jackson <ajax@redhat.com> 2.0.0-1
- Update to 2.0.0.

* Mon Mar 12 2007 Adam Jackson <ajax@redhat.com> 1.99.1-2
- nv.xinf: Various G73 PCI IDs.

* Fri Mar 09 2007 Adam Jackson <ajax@redhat.com> 1.99.1-1
- Update to nv 1.99.1, adds G80 support (wooooo!)
- nv.xinf: Add the G80 PCI IDs.

* Tue Feb 27 2007 Adam Jackson <ajax@redhat.com> 1.2.2.1-4
- nouveau update: Fix a typo that would cause a crash if anyone was insane
  enough to still be using an nv3 card.

* Thu Feb 15 2007 Adam Jackson <ajax@redhat.com> 1.2.2.1-3
- Initial nouveau driver build.  Utterly untested.

* Mon Feb 05 2007 Adam Jackson <ajax@redhat.com> 1.2.2.1-2
- nv.xinf: Update PCI IDs. (#227346)

* Fri Jan 05 2007 Adam Jackson <ajax@redhat.com> 1.2.2.1-1
- Update to 1.2.2.1

* Fri Dec 1 2006 Adam Jackson <ajax@redhat.com> 1.2.1-1
- Update to 1.2.1

* Thu Aug 31 2006 Adam Jackson <ajackson@redhat.com> 1.2.0-4.fc6
- nv-1.2.0-panel-range-hack: If we detect a panel, but don't get DDC, adjust
  the monitor's sync ranges to accomodate a 60Hz mode at the panel's
  native resolution.

* Wed Aug  2 2006 Adam Jackson <ajackson@redhat.com> 1.2.0-3.fc6
- Bump for upgrade path from FC5.

* Mon Jul 24 2006 Adam Jackson <ajackson@redhat.com> 1.2.0-2.fc6
- Update nv.xinf: Add about 30 new cards, disable a handful that pci.ids
  says aren't video cards, and comments galore.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> 1.2.0-1.1.fc6
- rebuild

* Fri Jul  7 2006 Adam Jackson <ajackson@redhat.com> 1.2.0-1.fc6
- Add %{?dist} and rebuild.

* Thu Jul  6 2006 Adam Jackson <ajackson@redhat.com> 1.2.0-1
- Update to 1.2.0: GeForce 6 and 7 updates and new hardware support.

* Mon Jun 26 2006 Adam Jackson <ajackson@redhat.com> 1.1.2-2
- Make the message printed when modes are rejected for not fitting in the
  panel size more accurate (and quieter).

* Sat Jun 17 2006 Mike A. Harris <mharris@redhat.com> 1.1.2-1
- Update to 1.1.2 release for X11R7.1 server.

* Wed Jun 14 2006 Adam Jackson <ajackson@redhat.com> 1.1.1-5
- Fix the panel tweak for a Toshiba laptop.

* Sat Jun 10 2006 Mike A. Harris <mharris@redhat.com> 1.1.1-4
- Added 10DE:0184 to nv.xinf, although the driver is not currently aware of
  this specific chip ID, the fallback code appears to work in bug #(186343)

* Tue May 23 2006 Adam Jackson <ajackson@redhat.com> 1.1.1-3
- Rebuild for 7.1 ABI fix.

* Mon Apr 10 2006 Adam Jackson <ajackson@redhat.com> 1.1.1-2
- Bump to appease beehive.

* Sun Apr 09 2006 Adam Jackson <ajackson@redhat.com> 1.1.1-1
- Update to 1.1.1 from 7.1RC1.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> 1.0.1.5-3.1
- bump again for double-long bug on ppc(64)

* Thu Feb 09 2006 Mike A. Harris <mharris@redhat.com> 1.0.1.5-3
- Added nv-1.0.1.5-updateto-cvs20050209.patch to sync driver with CVS and pick
  up support for newer Nvidia chips, and RandR rotation support.  (#180101)

* Thu Feb 09 2006 Mike A. Harris <mharris@redhat.com> 1.0.1.5-2
- Syncronized nv.xinf with nv_driver.c PCI ID list, including 10DE:0092 and
  10DE:00F2 for bug (#179997).

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> 1.0.1.5-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 18 2006 Mike A. Harris <mharris@redhat.com> 1.0.1.5-1
- Updated xorg-x11-drv-nv to version 1.0.1.5 from X11R7.0

* Tue Dec 20 2005 Mike A. Harris <mharris@redhat.com> 1.0.1.4-1
- Updated xorg-x11-drv-nv to version 1.0.1.4 from X11R7 RC4
- Removed 'x' suffix from manpage dirs to match RC4 upstream.

* Wed Nov 16 2005 Mike A. Harris <mharris@redhat.com> 1.0.1.2-1
- Updated xorg-x11-drv-nv to version 1.0.1.2 from X11R7 RC2

* Fri Nov 04 2005 Mike A. Harris <mharris@redhat.com> 1.0.1.1-1
- Updated xorg-x11-drv-nv to version 1.0.1.1 from X11R7 RC1
- Fix *.la file removal.
- Add riva128.so subdriver to file manifest.

* Mon Oct 03 2005 Mike A. Harris <mharris@redhat.com> 1.0.1-1
- Update BuildRoot to use Fedora Packaging Guidelines.
- Deglob file manifest.
- Limit "ExclusiveArch" to x86, x86_64, ia64, ppc

* Fri Sep 02 2005 Mike A. Harris <mharris@redhat.com> 1.0.1-0
- Initial spec file for nv video driver generated automatically
  by my xorg-driverspecgen script.
