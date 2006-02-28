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

%if %{without kernel}
%undefine	with_dist_kernel
%endif

%define		_rel	1
Summary:	Linux driver for drm
Summary(pl):	Sterownik dla Linuksa do drm
Name:		kernel-video-drm
Version:	20051020
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL v2
Group:		Base/Kernel
Source0:	drm-%{version}.tar.bz2
# Source0-md5:	a82d473de399da966b2562e67faedcaf
Patch0:		%{name}-pciids.patch
URL:		http://dri.freedesktop.org/
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel-module-build >= 2.6.7}
BuildRequires:	rpmbuild(macros) >= 1.217
%endif
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_up
Requires(postun):	%releq_kernel_up
%endif
Obsoletes:	kernel-drm = %{_kernel_ver_str}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is driver for drm for Linux.

This package contains Linux module.

%description -l pl
Sterownik dla Linuksa do drm.

Ten pakiet zawiera modu³ j±dra Linuksa.

%package -n kernel-smp-video-drm
Summary:	Linux SMP driver for drm
Summary(pl):	Sterownik dla Linuksa SMP do drm
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
This is driver for drm for Linux.

This package contains Linux SMP module.

%description -n kernel-smp-video-drm -l pl
Sterownik dla Linuksa do drm.

Ten pakiet zawiera modu³ j±dra Linuksa SMP.

%prep
%setup -q -n drm
%patch0 -p1

%build
  %if %{with kernel}

cd linux-core
install -d {ko-up,ko-smp}

# kernel module(s)
for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
	if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
		exit 1
	fi
	rm -rf include/{linux,config,asm}
        rm -f .config
	install -d include/{linux,config}
	ln -sf %{_kernelsrcdir}/config-$cfg .config
	ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h include/linux/autoconf.h
	ln -sf %{_kernelsrcdir}/include/asm-%{_target_base_arch} include/asm
	touch include/config/MARKER

	%{__make} M="$PWD" O="$PWD" drm_pciids.h
	%{__make} -C %{_kernelsrcdir} modules \
		CC="%{__cc}" CPP="%{__cpp}" \
		M="$PWD" O="$PWD" \
		SUBDIRS="$PWD" DRMSRCDIR="$PWD" \
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
