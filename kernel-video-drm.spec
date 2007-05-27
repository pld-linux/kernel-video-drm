#
# TODO:
# - make licensing clear (especially for the firmware)
# - optflags for apps
#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_with	verbose		# verbose build (V=1)

%if !%{with kernel}
%undefine	with_dist_kernel
%endif

%define		_rel	1
Summary:	Linux driver for DRM
Summary(pl.UTF-8):	Sterownik dla Linuksa do DRM
Name:		kernel%{_alt_kernel}-video-drm
Version:	20070527
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL v2
Group:		Base/Kernel
Source0:	drm-%{version}.tar.bz2
# Source0-md5:	dc2deb74a48ac9d7a9512c4b9f5efa23
URL:		http://dri.freedesktop.org/wiki/DRM
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRequires:	rpmbuild(macros) >= 1.379
%endif
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
Obsoletes:	kernel-drm = %{_kernel_ver_str}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The DRM (Direct Rendering Manager) is a Linux kernel module that gives
direct hardware access to DRI clients.

%description -l pl.UTF-8
DRM (Direct Rendering Manager) to moduł jądra Linuksa dający
bezpośredni dostęp do sprzętu klientom DRI.

%prep
%setup -q -n drm

%build
%if %{with kernel}
chmod u+x scripts/create_linux_pci_lists.sh
cd linux-core
cat ../shared-core/drm_pciids.txt | ../scripts/create_linux_pci_lists.sh
echo CONFIG_X86_CMPXCHG:=y >> Makefile.new
cat Makefile >> Makefile.new
mv Makefile.new Makefile
export DRMSRCDIR=`pwd`
%build_kernel_modules -m drm,mga,radeon,via,i810,nouveau,savage,i915,nv,sis,mach64,r128,tdfx
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with kernel}
%install_kernel_modules -m linux-core/{drm,mga,radeon,via,i810,nouveau,savage,i915,nv,sis,mach64,r128,tdfx} -d video
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-video-drm
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-video-drm
%depmod %{_kernel_ver}

%if %{with kernel}
%files -n kernel%{_alt_kernel}-video-drm
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/video/*.ko*
%endif
