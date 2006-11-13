#
# TODO:
# - make licensing clear (especially for the firmware)
# - optflags for apps
#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	smp		# don't build SMP module
%bcond_with	verbose		# verbose build (V=1)

%if !%{with kernel}
%undefine	with_dist_kernel
%endif

%define		_rel	1
Summary:	Linux driver for DRM
Summary(pl):	Sterownik dla Linuksa do DRM
Name:		kernel-video-drm
Version:	20060405
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL v2
Group:		Base/Kernel
Source0:	drm-%{version}.tar.bz2
# Source0-md5:	fb1c8734c7f128383b2578a2a793f524
URL:		http://dri.freedesktop.org/wiki/DRM
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel-module-build >= 3:2.6.14}
BuildRequires:	rpmbuild(macros) >= 1.286
%endif
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_up
Requires(postun):	%releq_kernel_up
%endif
Obsoletes:	kernel-drm = %{_kernel_ver_str}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The DRM (Direct Rendering Manager) is a Linux kernel module that gives
direct hardware access to DRI clients.

%description -l pl
DRM (Direct Rendering Manager) to modu³ j±dra Linuksa daj±cy
bezpo¶redni dostêp do sprzêtu klientom DRI.

%package -n kernel-smp-video-drm
Summary:	Linux SMP driver for DRM
Summary(pl):	Sterownik dla Linuksa SMP do DRM
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL v2
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_smp
Requires(postun):	%releq_kernel_smp
%endif
Obsoletes:	kernel-smp-drm = %{_kernel_ver_str}

%description -n kernel-smp-video-drm
The DRM (Direct Rendering Manager) is a Linux kernel module that gives
direct hardware access to DRI clients.

This package contains Linux SMP module.

%description -n kernel-smp-video-drm -l pl
DRM (Direct Rendering Manager) to modu³ j±dra Linuksa daj±cy
bezpo¶redni dostêp do sprzêtu klientom DRI.

Ten pakiet zawiera modu³ j±dra Linuksa SMP.

%prep
%setup -q -n drm

%build
%if %{with kernel}

cd linux-core
install -d {ko-up,ko-smp}

# kernel module(s)
for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
	if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
		exit 1
	fi

	rm -f *.o
	install -d o/include/linux
	ln -sf %{_kernelsrcdir}/config-$cfg o/.config
	ln -sf %{_kernelsrcdir}/Module.symvers-$cfg o/Module.symvers
	ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h o/include/linux/autoconf.h
%if %{with dist_kernel}
	%{__make} -j1 -C %{_kernelsrcdir} O=$PWD/o prepare scripts
%else
	install -d o/include/config
	touch o/include/config/MARKER
	ln -sf %{_kernelsrcdir}/scripts o/scripts
%endif

	%{__make} -C %{_kernelsrcdir} modules \
		CC="%{__cc}" CPP="%{__cpp}" \
		SYSSRC=%{_kernelsrcdir} \
		SYSOUT=$PWD/o \
		M=$PWD O=$PWD/o \
		DRMSRCDIR="$PWD" LINUXDIR=%{_kernelsrcdir} \
		%{?with_verbose:V=1}

	mv *.ko ko-$cfg
done
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with kernel}
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/video
cp linux-core/ko-%{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}/*.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/video
%if %{with smp} && %{with dist_kernel}
cp linux-core/ko-smp/*.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/video
%endif
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel-video-drm
%depmod %{_kernel_ver}

%postun	-n kernel-video-drm
%depmod %{_kernel_ver}

%post	-n kernel-smp-video-drm
%depmod %{_kernel_ver}smp

%postun	-n kernel-smp-video-drm
%depmod %{_kernel_ver}smp

%if %{with kernel}
%files -n kernel-video-drm
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/video/*.ko*

%if %{with smp} && %{with dist_kernel}
%files -n kernel-smp-video-drm
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/video/*.ko*
%endif
%endif
