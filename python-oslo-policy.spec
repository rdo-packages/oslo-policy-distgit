# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global pypi_name oslo.policy
%global pkg_name oslo-policy
%global with_doc 1
%global common_desc \
An OpenStack library for policy.

%global common_desc1 \
Test subpackage for the Oslo policy library.

Name:           python-%{pkg_name}
Version:        2.1.2
Release:        1%{?dist}
Summary:        OpenStack oslo.policy library

License:        ASL 2.0
URL:            https://launchpad.net/oslo
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
BuildArch:      noarch

%description
%{common_desc}

%package -n python%{pyver}-%{pkg_name}
Summary:        OpenStack oslo.policy library
%{?python_provide:%python_provide python%{pyver}-%{pkg_name}}
%if %{pyver} == 3
Obsoletes: python2-%{pkg_name} < %{version}-%{release}
%endif

BuildRequires:  git
BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-pbr
# test dependencies
BuildRequires:  python%{pyver}-hacking
BuildRequires:  python%{pyver}-oslo-config
BuildRequires:  python%{pyver}-oslo-context
BuildRequires:  python%{pyver}-oslo-serialization
BuildRequires:  python%{pyver}-oslotest
BuildRequires:  python%{pyver}-fixtures
BuildRequires:  python%{pyver}-mock
BuildRequires:  python%{pyver}-requests
BuildRequires:  python%{pyver}-stevedore
BuildRequires:  python%{pyver}-stestr
BuildRequires:  python%{pyver}-sphinx
# Required to compile translation files
BuildRequires:  python%{pyver}-babel

# Handle python2 exception
%if %{pyver} == 2
BuildRequires:  python-requests-mock
BuildRequires:  python-docutils
BuildRequires:  PyYAML >= 3.1.0
%else
BuildRequires:  python%{pyver}-requests-mock
BuildRequires:  python%{pyver}-docutils
BuildRequires:  python%{pyver}-PyYAML >= 3.1.0
%endif

Requires:       python%{pyver}-requests
Requires:       python%{pyver}-oslo-config >= 2:5.2.0
Requires:       python%{pyver}-oslo-context >= 2.22.0
Requires:       python%{pyver}-oslo-i18n >= 3.15.3
Requires:       python%{pyver}-oslo-serialization >= 2.18.0
Requires:       python%{pyver}-six >= 1.10.0
Requires:       python%{pyver}-stevedore >= 1.20.0

# Handle python2 exception
%if %{pyver} == 2
Requires:  PyYAML >= 3.1.0
%else
Requires:  python%{pyver}-PyYAML >= 3.1.0
%endif
Requires:       python-%{pkg_name}-lang = %{version}-%{release}

%description -n python%{pyver}-%{pkg_name}
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{pkg_name}-doc
Summary:    Documentation for the Oslo policy library

BuildRequires:  python%{pyver}-sphinx
BuildRequires:  python%{pyver}-openstackdocstheme
BuildRequires:  python%{pyver}-oslo-i18n

%description -n python-%{pkg_name}-doc
Documentation for the Oslo policy library.
%endif

%package -n python%{pyver}-%{pkg_name}-tests
Summary:    Test subpackage for the Oslo policy library
%{?python_provide:%python_provide python%{pyver}-%{pkg_name}}

Requires:  python%{pyver}-%{pkg_name} = %{version}-%{release}
Requires:  python%{pyver}-hacking
Requires:  python%{pyver}-oslotest
Requires:  python%{pyver}-fixtures
Requires:  python%{pyver}-mock
Requires:  python%{pyver}-requests

# Handle python2 exception
%if %{pyver} == 2
Requires:  python-requests-mock
%else
Requires:  python%{pyver}-requests-mock
%endif

%description -n python%{pyver}-%{pkg_name}-tests
%{common_desc1}

%package  -n python-%{pkg_name}-lang
Summary:   Translation files for Oslo policy library

%description -n python-%{pkg_name}-lang
Translation files for Oslo policy library

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git
# Let RPM handle the dependencies
rm -f *requirements.txt

# FIXME (jpena): Remove buggy PO-Revision-Date lines in translation
# See https://bugs.launchpad.net/openstack-i18n/+bug/1586041 for details
sed -i '/^\"PO-Revision-Date: \\n\"/d' oslo_policy/locale/*/LC_MESSAGES/*.po

%build
%{pyver_build}

%if 0%{?with_doc}
# generate html docs
%{pyver_bin} setup.py build_sphinx -b html
# Fix hidden-file-or-dir warnings
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

# Generate i18n files
%{pyver_bin} setup.py compile_catalog -d build/lib/oslo_policy/locale

%install
%{pyver_install}
pushd %{buildroot}/%{_bindir}
for item in checker list-redundant policy-generator sample-generator
do
  # Create a versioned binary for backwards compatibility until everything is pure py3
  ln -s oslopolicy-$item %{buildroot}%{_bindir}/oslopolicy-$item-%{pyver}
done
popd

# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{pyver_sitelib}/oslo_policy/locale/*/LC_*/oslo_policy*po
rm -f %{buildroot}%{pyver_sitelib}/oslo_policy/locale/*pot
mv %{buildroot}%{pyver_sitelib}/oslo_policy/locale %{buildroot}%{_datadir}/locale

# Find language files
%find_lang oslo_policy --all-name

%check
export OS_TEST_PATH="./oslo_policy/tests"
stestr-%{pyver} --test-path $OS_TEST_PATH run

%files -n python%{pyver}-%{pkg_name}
%doc README.rst
%license LICENSE
%{_bindir}/oslopolicy-policy-upgrade
%{_bindir}/oslopolicy-checker
%{_bindir}/oslopolicy-checker-%{pyver}
%{_bindir}/oslopolicy-list-redundant
%{_bindir}/oslopolicy-list-redundant-%{pyver}
%{_bindir}/oslopolicy-policy-generator
%{_bindir}/oslopolicy-policy-generator-%{pyver}
%{_bindir}/oslopolicy-sample-generator
%{_bindir}/oslopolicy-sample-generator-%{pyver}
%{pyver_sitelib}/oslo_policy
%{pyver_sitelib}/*.egg-info
%exclude %{pyver_sitelib}/oslo_policy/tests

%if 0%{?with_doc}
%files -n python-%{pkg_name}-doc
%doc doc/build/html
%license LICENSE
%endif

%files -n python%{pyver}-%{pkg_name}-tests
%{pyver_sitelib}/oslo_policy/tests

%files -n python-%{pkg_name}-lang -f oslo_policy.lang
%license LICENSE

%changelog
* Mon Jan 13 2020 RDO <dev@lists.rdoproject.org> 2.1.2-1
- Update to 2.1.2

* Fri Mar 08 2019 RDO <dev@lists.rdoproject.org> 2.1.1-1
- Update to 2.1.1

