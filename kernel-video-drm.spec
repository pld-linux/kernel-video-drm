#
# TODO:
# - make licensing clear (especially for the firmware)
# - optflags for apps
#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_with	verbose         # verbose build (V=1)

%define		_rel	2
Summary:	Linux driver for DRM
Summary(pl.UTF-8):	Sterownik dla Linuksa do DRM
Name:		kernel%{_alt_kernel}-video-drm
Version:	20090331
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL v2
Group:		Base/Kernel
# git clone --depth 1 git://anongit.freedesktop.org/git/mesa/drm kernel-video-drm
# cd kernel-video-drm
# git archive master --prefix drm/ | bzip2 > drm-$(date +%Y%m%d).tar.bz2
Source0:	drm-%{version}.tar.bz2
# Source0-md5:	968740b4883bf219cf831f585184f614
URL:		http://dri.freedesktop.org/wiki/DRM
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRequires:	rpmbuild(macros) >= 1.379
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
Obsoletes:	kernel-drm = %{_kernel_ver_str}
Conflicts:	kernel-drm = %{_kernel_ver_str}
%endif
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
chmod u+x scripts/create_linux_pci_lists.sh
cd linux-core
cat ../shared-core/drm_pciids.txt | ../scripts/create_linux_pci_lists.sh
echo CONFIG_X86_CMPXCHG:=y >> Makefile.new
cat Makefile >> Makefile.new
mv Makefile.new Makefile
export DRMSRCDIR=`pwd`
%ifarch ppc ppc64
%build_kernel_modules -m drm,mach64,mga,nouveau,r128,radeon,savage,sis,tdfx,via,xgi
%else
%build_kernel_modules -m drm,i810,mach64,mga,nouveau,r128,radeon,savage,sis,tdfx,via,xgi
%endif

%install
rm -rf $RPM_BUILD_ROOT

%ifarch ppc ppc64
%install_kernel_modules -m linux-core/{drm,mach64,mga,nouveau,r128,radeon,savage,sis,tdfx,via,xgi} -d kernel/drivers/gpu/drm
%else
%install_kernel_modules -m linux-core/{drm,i810,mach64,mga,nouveau,r128,radeon,savage,sis,tdfx,via,xgi} -d kernel/drivers/gpu/drm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-video-drm
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-video-drm
%depmod %{_kernel_ver}

%files -n kernel%{_alt_kernel}-video-drm
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/kernel/drivers/gpu
